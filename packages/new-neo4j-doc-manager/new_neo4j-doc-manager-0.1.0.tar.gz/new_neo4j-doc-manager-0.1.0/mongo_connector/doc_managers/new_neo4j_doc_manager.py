# -*- coding: utf-8 -*-
# @Time    : 2022/4/24 上午11:08
# @Author  : kyq
# @Software: PyCharm


import base64
import logging
import os
import os.path as path, sys

import bson.json_util

from mongo_connector.doc_managers.nodes_and_relationships_builder import NodesAndRelationshipsBuilder
from mongo_connector.doc_managers.nodes_and_relationships_updater import NodesAndRelationshipsUpdater

from py2neo import Graph,NodeMatcher

from mongo_connector.compat import u
from mongo_connector.constants import (DEFAULT_COMMIT_INTERVAL,DEFAULT_MAX_BULK)
from mongo_connector.util import exception_wrapper, retry_until_ok
from mongo_connector.doc_managers.doc_manager_base import DocManagerBase
from mongo_connector.doc_managers.formatters import DefaultDocumentFormatter



LOG = logging.getLogger(__name__)


class DocManager(DocManagerBase):
    """
    Neo4j implementation for the DocManager. Receives documents and
    communicates with Neo4j Server.
    """

    def __init__(self, url, auto_commit_interval=DEFAULT_COMMIT_INTERVAL,
                 unique_key='_id', chunk_size=DEFAULT_MAX_BULK, **kwargs):

        self.graph = Graph('http://192.168.3.215:7474/db/data')
        self.auto_commit_interval = auto_commit_interval
        self.unique_key = unique_key
        self.chunk_size = chunk_size
        self._formatter = DefaultDocumentFormatter()
        self.kwargs = kwargs.get("clientOptions")
        self.actor = []
        self.director = []

    def apply_id_constraint(self, doc_types):
        for doc_type in doc_types:
            constraint = "CREATE CONSTRAINT ON (d:`{doc_type}`) ASSERT d._id IS UNIQUE".format(doc_type=doc_type)
            self.graph.cypher.execute(constraint)

    def stop(self):
        """Stop the auto-commit thread."""
        self.auto_commit_interval = None

    def upsert(self, doc):
        """Inserts a document into Neo4j."""
        doc_id = u(doc.pop("_id"))
        doc = self._formatter.format_document(doc)
        builder = NodesAndRelationshipsBuilder(doc,doc_id)
        tx = self.graph.begin()
        for director in builder.director_list:
            for statement in director.keys():
                name = director[statement]['actorName']
                ret = self.nodeExist(name)
                if ret == False:
                    tx.run(statement, {"parameters": director[statement]})
                else:
                    self.director.append(ret)

        for cast in builder.cast_list:
            for statement in cast.keys():
                name = cast[statement]['actorName']
                ret = self.nodeExist(name)
                if ret == False:
                    tx.run(statement, {"parameters": cast[statement]})
                else:
                    self.actor.append(ret)

        for director_ in builder.director_list:
            for director in director_.keys():
                for actor_ in builder.cast_list:
                    for actor in actor_.keys():
                        id = director_[director]['doubanId']
                        id_ = actor_[actor]['doubanId']
                        program_id = builder.parameters['programId']
                        type = "{" + " program_id:{},count:1".format([program_id]) + "}"
                        tx.run(self.creat_relationship(id, id_, type,program_id))
        tx.commit()

    def bulk_upsert(self, docs, namespace, timestamp):
        """Insert multiple documents into Neo4j."""
        """Maximum chunk size is 1000. Transaction blocks won't have more than 1000 statements."""
        metadata = {"_ts": timestamp}
        tx = self.graph.cypher.begin()
        for doc in docs:
            index, doc_type = self._index_and_mapping(namespace)
            doc_id = u(doc.pop("_id"))
            doc = self._formatter.format_document(doc)
            builder = NodesAndRelationshipsBuilder(doc, doc_type, doc_id, metadata)
            self.apply_id_constraint(builder.doc_types)
            for statement in builder.query_nodes.keys():
                tx.append(statement, builder.query_nodes[statement])
            for relationship in builder.relationships_query.keys():
                tx.append(relationship, builder.relationships_query[relationship])
        tx.commit()


    def commit(self):
        LOG.error("Commit")

    def nodeExist(self, name):
        matcher = NodeMatcher(self.graph)
        m = matcher.match().where(actorName=name).first()
        if m is None:
            return False
        else:
            return m

    def creat_relationship(self,id, doubanid, a,program_id):
        doubanId = "{" + "doubanId:'{}'".format(id) + "}"
        a=a
        director_doubanId = "{" + "doubanId:'{}'".format(doubanid) + "}"
        statement = 'MATCH (n{a}),(n1{b}),p=(n)-[r:Director_Actor]-(n1)  return r.count'.format(a=doubanId, b=director_doubanId)
        count = self.graph.begin().run(statement).data()
        if count != []:
            statement = 'MATCH (n{a}),(n1{b}),p=(n)-[r:Director_Actor]-(n1)  return r.program_id'.format(a=doubanId,b=director_doubanId)
            programId = self.graph.begin().run(statement).data()
            program_id = program_id
            programId_ = programId[0]['r.program_id']
            if program_id in programId_:
                count = count[0]['r.count']
            else:
                count = count[0]['r.count'] + 1
            programId_.append(program_id)
            statement = 'MATCH (n{a}),(n1{b}),p=(n)-[r:Director_Actor]-(n1) set r.count={c}, r.program_id={d} return r'.format(
                a=doubanId, b=director_doubanId, c=count, d=list(set(programId_)))
        else:
            statement = 'MATCH (director{a}), (actor{b}) CREATE (director)-[r:Director_Actor {c}]->(actor)'.format(a=director_doubanId, b=doubanId, c=a)
        return statement

    # def creat_relationship1(self,id, doubanid, a):
    #     doubanId = "{" + "doubanId:'{}'".format(id) + "}"
    #     director_doubanId = "{" + "doubanId:'{}'".format(doubanid) + "}"
    #     statement = 'MATCH (actor{a}), (director{b}) CREATE (actor)-[r:Actor_Director {c}]->(director)'.format(a=director_doubanId, b=doubanId, c=a)
    #     return statement
