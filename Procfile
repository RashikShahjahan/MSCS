heroku ps:scale web=1
web: uvicorn app:app --host=0.0.0.0 --port=${PORT:-5000}
heroku config:set MONGODB_URI="mongodb+srv://iamrashiktoo:mythology@cluster0.vzwx6zx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"