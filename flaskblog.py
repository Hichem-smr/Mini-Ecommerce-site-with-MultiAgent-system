from flask import Flask, render_template, url_for, request
import time
from pkg_resources import to_filename
from spade import agent, quit_spade,web
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
from spade.template import Template
from pprint import pprint
import json
import time
app = Flask(__name__)

posts = []
posts_filtered = []

class fenderAgent(agent.Agent):
    class InformBehav(OneShotBehaviour):
        async def run(self):
            msg = Message(to="central@localhost", sender="fender@localhost", body=str(fenderAgent.guitars() + fenderAgent.amps() + fenderAgent.bass()))
            await self.send(msg)

    class sellProduct(CyclicBehaviour):
        async def run(self):	
            msg = await self.receive(timeout=15)
            if msg: 
                name = msg.body.split("")[1]
                quantity = msg.body.split("")[0]
                inst = msg.body.split("")[2]
                f = open('Fender/Database.json')
                f.close()
                Fender = json.load(f)
                for inst in Fender[inst]:
                    if(inst["name"] == name):
                        inst['quantity'] = inst['quantity'] - quantity

                with open('Fender/Database.json', 'w') as fp:
                    json.dumps(Fender, indent=4)

    async def setup(self):
        b = self.InformBehav()
        self.add_behaviour(b)
        a = self.sellProduct()
        self.add_behaviour(a)

    def guitars():
        f = open('Fender/Database.json')
        fender = json.load(f)
        return fender['Guitar']

    def amps():
        f = open('Fender/Database.json')
        fender = json.load(f)
        f.close()
        return fender['Amp']

    def bass():
        f = open('Fender/Database.json')
        fender = json.load(f)
        f.close()
        return fender['bass']

class musicmanAgent(agent.Agent):
    class InformBehav(OneShotBehaviour):
        async def run(self):
            msg = Message(to="central@localhost", sender="musicman@localhost", body=str(musicmanAgent.guitars() + musicmanAgent.amps() + musicmanAgent.bass()))
            await self.send(msg)

    class sellProduct(CyclicBehaviour):
        async def run(self):	
            msg = await self.receive(timeout=15)
            if msg: 
                name = msg.body.split("")[1]
                quantity = msg.body.split("")[0]
                inst = msg.body.split("")[2]
                f = open('musicman/Database.json')
                f.close()
                musicman = json.load(f)
                for inst in musicman[inst]:
                    if(inst["name"] == name):
                        inst['quantity'] = inst['quantity'] - quantity

                with open('musicman/Database.json', 'w') as fp:
                    json.dumps(musicman, indent=4)
    
    async def setup(self):
        b = self.InformBehav()
        self.add_behaviour(b)
        a = self.sellProduct()
        self.add_behaviour(a)

    def guitars():
        f = open('Musicman/Database.json')
        Musicman = json.load(f)
        return Musicman['Guitar']

    def amps():
        f = open('Musicman/Database.json')
        Musicman = json.load(f)
        f.close()
        return Musicman['Amp']

    def bass():
        f = open('Musicman/Database.json')
        Musicman = json.load(f)
        f.close()
        return Musicman['bass']

class YamahaAgent(agent.Agent):
    class InformBehav(OneShotBehaviour):
        async def run(self):
            msg = Message(to="central@localhost", sender="yamaha@localhost", body=str(YamahaAgent.guitars() + YamahaAgent.amps() + YamahaAgent.bass()))
            await self.send(msg)
    
    class sellProduct(CyclicBehaviour):
        async def run(self):	
            msg = await self.receive(timeout=15)
            if msg: 
                name = msg.body.split("")[1]
                quantity = msg.body.split("")[0]
                inst = msg.body.split("")[2]
                f = open('Yamaha/Database.json')
                f.close()
                Yamaha = json.load(f)
                for inst in Yamaha[inst]:
                    if(inst["name"] == name):
                        inst['quantity'] = inst['quantity'] - quantity

                with open('Yamaha/Database.json', 'w') as fp:
                    json.dumps(Yamaha, indent=4)

    async def setup(self):
        b = self.InformBehav()
        self.add_behaviour(b)
        a = self.sellProduct()
        self.add_behaviour(a)

    def guitars():
        f = open('Yamaha/Database.json')
        Yamaha = json.load(f)
        return Yamaha['Guitar']

    def amps():
        f = open('Yamaha/Database.json')
        Yamaha = json.load(f)
        f.close()
        return Yamaha['Amp']

    def bass():
        f = open('Yamaha/Database.json')
        Yamaha = json.load(f)
        f.close()
        return Yamaha['bass']

class centralagent(agent.Agent):
    class RecvBehav(CyclicBehaviour):
        async def run(self):	
            global posts
            print("RecvBehav running")
            msg = await self.receive(timeout=15)
            if msg: 
                list = json.loads(msg.body.replace("\'", "\""))
                if(list[0] not in posts):
                    posts += list

    async def setup(self):
        if(len(posts) == 0):
            b = self.RecvBehav()
            template = Template()
            self.add_behaviour(b, template)

class BuyingAgent(agent.Agent):
    # class BuyProduct(OneShotBehaviour):
    #     async def run(self):	
    #         if(brand == "Fender"):
    #             msg = Message(to_filename="fender@localhost", body=str(quantity) + " " + name + " " + inst)
    #             await self.send(msg)
    #         elif(brand == "Yamaha"):
    #             msg = Message(to="yamaha@localhost", body=str(quantity) + " " + name + " " + inst)
    #             await self.send(msg)
    #         elif(brand == "Musicman"):
    #             msg = Message(to="musicman@localhost", body=str(quantity) + " " + name + " " + inst)
    #             await self.send(msg)

    async def setup(self):
        b = self.BuyProduct()
        template = Template()
        self.add_behaviour(b, template)

@app.route("/")
@app.route("/home")
def Products():

    if(len(posts) == 0):
        central = centralagent("central@localhost", "")
        fender = fenderAgent("fender@localhost", "")
        Musicman = musicmanAgent("musicman@localhost","")
        Yamaha = YamahaAgent("yamaha@localhost","")

        recieving_pool = central.start()
        recieving_pool.result()

        sending_fender = fender.start()
        sending_fender.result()

        sending_musicman = Musicman.start()
        sending_musicman.result()

        sending_Yamaha = Yamaha.start()
        sending_Yamaha.result()



    return render_template('Products.html',title='All Products', posts=posts)


@app.route("/Amps")
def Amps():
    return render_template('Amps.html', title='Amps')

@app.route("/submit", methods=['GET', 'POST'])
def submit():
    brand = request.form.get('brand')
    price = request.form.get('Price')
    inst = request.form.get('Instrument')
    type = request.form.get('Type')
    color = request.form.get('Color')
    
    def brand_filter(posts, brand):
        if brand == "None":
            return posts
        else:
            for post in posts:
                if(post['brand'] == brand):
                    yield post

    def inst_filter(posts, inst):
        if inst == "None":
            return posts
        else:
            for post in posts:
                if(post['instrument'] == inst):
                    yield post

    def type_filter(posts, type):
        if type == "None":
            return posts
        else:
            for post in posts:
                if(post['type'] == type):
                    yield post

    def color_filter(posts, color):
        if color == "None":
            return posts
        else:
            for post in posts:
                if(post['color'] == color):
                    yield post

    def price_filter(posts, price):
        if price == "None":
            return posts
        else:
                if price == 1:
                    for post in posts:
                        if(int(post['price']) < 250):
                            print(int(post['price']))
                            yield post
                elif price == 2:
                    for post in posts:
                        if(int(post['price']) > 250 and int(post['price']) < 1000):
                            yield post
                elif price == 3:
                    for post in posts:
                        if(int(post['price']) > 1000 and int(post['price']) < 2000):
                            yield post
                elif price == 4:
                    for post in posts:
                        if(int(post['price']) > 2000):
                            yield post
    filtered_posts = posts.copy()
    if(brand != "None"):
        filtered_posts = brand_filter(filtered_posts, brand)
    if(inst != "None"):
        filtered_posts = inst_filter(list(filtered_posts), inst)
    if(color != "None"):
        filtered_posts = color_filter(list(filtered_posts), color)
    if(type != "None"):
        filtered_posts = type_filter(list(filtered_posts), type)
    if(price != "None"):
        filtered_posts = price_filter(list(filtered_posts), int(price))

    filtered_posts = list(filtered_posts)
    return render_template('Products.html', posts=filtered_posts)

@app.route('/quantity_update', methods = ['POST', 'GET'])
def quantity_update():
    if request.method == "POST":
        print("im accessing")
        new_quantity = str(request.form['new_quantity'])
        brand = str(request.form['brand'])
        name = str(request.form['name'])
        print(new_quantity, name, brand)

        # BuyingAgt = BuyingAgent("yamaha@localhost","")
        # Buying_start = BuyingAgt.start()
        # Buying_start.result()

        return str(request.form['new_quantity'])

app.run(debug=True)


