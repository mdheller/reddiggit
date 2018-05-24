from flask import Flask
import reddiggit 

app = reddiggit.create_app()
app.run()
