import tornado.web, tornado.ioloop
import json

class HomePageHandler(tornado.web.RequestHandler):
    """class docstring"""
    def get(self):
        self.render('./static/html/index.html')
class DatabaseHandler(tornado.web.RequestHandler):
    def get(self):
        with open("./data.json") as datafile:
            data = json.load(datafile)
            self.write(json.dumps(data))

    def post(self):
        with open("./data.json", "r+") as datafile:
            db = json.load(datafile)
            new_data = {
                "id": len(db) + 1, 
                "first": self.get_argument("first"),
                "last": self.get_argument("last"),
                "number": self.get_argument( "number"),
                "email": self.get_argument("email")
                }
            db.append(new_data)

        with open("./data.json", "w+") as datafile:
            try:
                json.dump(db, datafile)
            except Exception as err:
                print("Some Error Occurred!")
                print(err)
        self.render('./static/html/index.html')
        
    def put(self):
        try:
            with open("./data.json") as df:
                db = json.load(df)
            for item in db:
                if item["id"] == int(self.get_argument("id")):
                    item["first"] = self.get_argument("first")
                    item["last"] = self.get_argument("last")
                    item["number"] = self.get_argument( "number")
                    item["email"] = self.get_argument("email")

            with open("./data.json", "w") as df:
                json.dump(db, df)
                self.write({"message": "Updated Successfully!"})

        except Exception as err:
            self.write({"message": f"Error description: {err}"})

    def delete(self):
        new_db = []
        with open("./data.json") as df:
            db = json.load(df)
            try:
                for item in db:
                    if item["id"] != int(self.get_argument("id")):
                        new_db.append(item)
            except Exception as err:
                self.write({"message": f"Delete Failed! {err}"})
        with open("./data.json", "w") as df:
            json.dump(new_db, df)
            self.write({"message": "Deleted Successfully!"})


class SearchResultsHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('./static/html/search.html')

class SearchDatabaseHandler(tornado.web.RequestHandler):
    def get(self):
        query_param = self.get_argument("first")
        data_result = []
        with open("./data.json") as df:
            db = json.load(df)
            for elem in db:
                if elem["first"].lower() == query_param.lower():
                    data_result.append(elem)
        self.write(json.dumps(data_result))
class searchWithResourceParamHandler(tornado.web.RequestHandler):
    def get(self, f=None, q=None):
        data_result = []
        print(f, q)
        with open("./data.json") as df:
            db = json.load(df)
            if f is None:
                self.write("Hi guest, welcome to Search Engine!")
            elif q is None:
                for elem in db:
                    if elem["first"].lower() == f.lower():
                        data_result.append(elem)
                self.write(f"hi {f}, here is your data:\n{json.dumps(data_result)}")
            else:
                for elem in db:
                    if elem["first"].lower() == f.lower():
                        if q in elem:
                            data_result.append({"first": elem["first"], f"{q}": elem[q]})
                self.write(f"hi {f}, here is your data:\n{json.dumps(data_result)}")

if __name__ == '__main__':
    PORT = 8882
    app = tornado.web.Application([
        (r"/", HomePageHandler),
        (r"/v1/data", DatabaseHandler),
        (r"/v1/search", SearchResultsHandler),
        (r"/v1/searchresults", SearchDatabaseHandler), # example of query params
        (r"/v1/contacts/([a-zA-Z]+)/([a-zA-Z]+)", searchWithResourceParamHandler)
    ])
    app.listen(PORT)
    print(f"Service is Ready! Using/listening on port: {PORT}.")
    tornado.ioloop.IOLoop.current().start()