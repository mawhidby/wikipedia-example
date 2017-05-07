#!/usr/bin/env python3

import wikipedia
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler, HTTPError
from tornado.httpclient import HTTPClient
import braid

# Location of the templates
TEMPLATE_DIR = "./templates"

class HomeHandler(RequestHandler):
    def get(self):
        if self.get_argument("action", None) == "get_article":
            article_name = self.get_argument("article")
            self.get_article(article_name)
        else:
            self.get_main()

    def get_article(self, article_name):
        trans = braid.Transaction()
        conn = wikipedia.get_connection()
        cursor = conn.cursor()

        # Get the ID of the article we want from its name
        article_id = wikipedia.get_article_id(cursor, article_name)

        if not article_id:
            raise HTTPError(404)

        # Get the vertex/edge data from braid. Everything except for the
        # article name metadata is fetched in a transaction for better
        # performance. We get article name metadata separately, because we need
        # to fetch the related vertex IDs first.
        vertex_query = braid.VertexQuery.vertex(article_id)
        trans.get_vertices(vertex_query)
        trans.get_edge_count(vertex_query.outbound_edges("link"))
        trans.get_edges(vertex_query.outbound_edges("link", limit=1000))
        client = wikipedia.get_client(cursor)
        [vertex_data, edge_count, edge_data] = client.transaction(trans)
        inbound_edge_ids = [e.key.inbound_id for e in edge_data]

        if inbound_edge_ids:
            inbound_edge_names = client.run_script("get_movie_names.lua", inbound_edge_ids)
        else:
            inbound_edge_names = {}
        
        self.render(
            "article.html",
            article_name=article_name,
            article_id=article_id,
            vertex_data=vertex_data[0],
            edge_count=edge_count,
            inbound_edge_ids=inbound_edge_ids,
            inbound_edge_names=inbound_edge_names
        )

    def get_main(self):
        self.render("main.html")

def main():
    with wikipedia.server():
        app = Application([
            (r"/", HomeHandler),
        ], **{
            "template_path": TEMPLATE_DIR
        })

        app.listen(8080)
        IOLoop.current().start()

if __name__ == "__main__":
    main()
