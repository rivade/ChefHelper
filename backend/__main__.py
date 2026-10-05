import mongo
import api
import uvicorn

if __name__ == "__main__":
    mongo.init()
    mongo.test_connection()
    
    app = api.init()
    
    uvicorn.run(app, host="0.0.0.0", port=8001)