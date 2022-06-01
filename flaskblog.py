from flask import Flask, render_template, url_for, request
import time
from pkg_resources import to_filename
from spade import agent, quit_spade,web
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
from spade.template import Template
from pprint import pprint
from dateutil.parser import parse 
import json
from collections import OrderedDict
import urllib
import time
app = Flask(__name__)

posts = []
posts_filtered = []
new_quantity = None
brand = None
name = None
inst = None
first_launch = 0
first_launch1 = 0
first_launch2 = 0
class fenderAgent(agent.Agent):
    class InformBehav(OneShotBehaviour):
        async def run(self):
            msg = Message(to="central@localhost", sender="fender@localhost", body=str(fenderAgent.guitars() + fenderAgent.amps() + fenderAgent.bass()))
            print("sending my message")
            await self.send(msg)

    class sellProduct(CyclicBehaviour):
        async def run(self):	
            msg = await self.receive(timeout=15)
            if msg: 
                name = msg.body.split(" ")[1]
                quantity = msg.body.split(" ")[0]
                inst = msg.body.split(" ")[2]
                print(name, quantity, inst)
                f = open('Fender/Database.json')
                Fender = json.load(f)
                f.close()

                if("Gui" in inst):
                    i = 'Guitar'
                elif("Amp" in inst):
                    i = 'Amp'
                elif("bass" in inst):
                    i = 'bass'

                for inst in Fender[i]:
                    if(str(inst["name"]) in name):
                        inst['quantity'] = int(quantity)
                        print("quantity updated!", inst['quantity'])

                with open('Fender/Database.json', 'w') as fp:
                    json.dump(Fender, fp,  indent=4)

    async def setup(self):
        global first_launch1
        b = self.InformBehav()
        self.add_behaviour(b)
        if first_launch1 == 0:
            first_launch1 = 1
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
                name = msg.body.split(" ")[1]
                quantity = msg.body.split(" ")[0]
                inst = msg.body.split(" ")[2]
                print(name, quantity, inst)
                f = open('Musicman/Database.json')
                musicman = json.load(f)
                f.close()

                if("Gui" in inst):
                    i = 'Guitar'
                elif("Amp" in inst):
                    i = 'Amp'
                elif("bass" in inst):
                    i = 'bass'

                for inst in musicman[i]:
                    if(str(inst["name"]) in name):
                        inst['quantity'] = int(quantity)
                        print("quantity updated!", inst['quantity'])

                with open('Musicman/Database.json', 'w') as fp:
                    json.dump(musicman, fp,  indent=4)
    
    async def setup(self):
        global first_launch2
        b = self.InformBehav()
        self.add_behaviour(b)
        if(first_launch2 == 0):
            first_launch2 = 1
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
                name = msg.body.split(" ")[1]
                quantity = msg.body.split(" ")[0]
                inst = msg.body.split(" ")[2]
                print(name, quantity, inst)
                f = open('Yamaha/Database.json')
                Yamaha = json.load(f)
                f.close()

                if("Gui" in inst):
                    i = 'Guitar'
                elif("Amp" in inst):
                    i = 'Amp'
                elif("bass" in inst):
                    i = 'bass'

                for inst in Yamaha[i]:
                    if(str(inst["name"]) in name):
                        inst['quantity'] = int(quantity)
                        print("quantity updated!", inst['quantity'])

                with open('Yamaha/Database.json', 'w') as fp:
                    json.dump(Yamaha, fp,  indent=4)

    async def setup(self):
        global first_launch
        b = self.InformBehav()
        self.add_behaviour(b)
        if(first_launch == 0):
            first_launch = 1
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
            msg = await self.receive(timeout=30)
            if msg: 
                print("got the message and it says")
                list = json.loads(msg.body.replace("\'", "\""))
                posts += list

    async def setup(self):
        b = self.RecvBehav()
        template = Template()
        self.add_behaviour(b, template)

class BuyingAgent(agent.Agent):
    class BuyProduct(OneShotBehaviour):
        async def run(self):	
            global new_quantity, name, brand, inst
            if("Fender" in brand.strip()):
                msg = Message(to="fender@localhost", body=str(new_quantity) + " " + name + " " + inst)
                await self.send(msg)
            elif("Yamaha" in brand.strip()):
                msg = Message(to="yamaha@localhost", body=str(new_quantity) + " " + name + " " + inst)
                await self.send(msg)
            elif("Musicman" in brand.strip()):
                msg = Message(to="musicman@localhost", body=str(new_quantity) + " " + name + " " + inst)
                await self.send(msg)

    async def setup(self):
        b = self.BuyProduct()
        self.add_behaviour(b)

fender = fenderAgent("fender@localhost", "")
Musicman = musicmanAgent("musicman@localhost","")
Yamaha = YamahaAgent("yamaha@localhost","")
central = centralagent("central@localhost", "")
recieving_pool = central.start()
recieving_pool.result()

@app.route("/")
# @app.route("/home")
def Products():
    global posts
    posts = []
    sending_fender = fender.start()
    sending_musicman = Musicman.start()
    sending_Yamaha = Yamaha.start()
    sending_fender.result()
    sending_musicman.result()
    sending_Yamaha.result()
    time.sleep(1)
    return render_template('Products.html',title='All Products', posts=posts)


@app.route("/Promotions")
def Promo():
    return render_template('Promotions.html', title='Promotions')

@app.route("/", methods=['GET', 'POST'])
def submit():
    global posts
    brand = request.form.get('brand')
    price = request.form.get('Price')
    inst = request.form.get('Instrument')
    type = request.form.get('Type')
    color = request.form.get('Color')
    order = request.form.get('Order')
    print("hi im the order", order)
    
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
                        if(int(post['price']) >= 250 and int(post['price']) < 1000):
                            yield post
                elif price == 3:
                    for post in posts:
                        if(int(post['price']) >= 1000 and int(post['price']) < 2000):
                            yield post
                elif price == 4:
                    for post in posts:
                        if(int(post['price']) >= 2000):
                            yield post

    def order_filter(posts, color):
        if(color == 1):
            posts = sorted(posts, key = lambda i: int(i['price']),reverse=True)
            return posts
        elif(color == 2):
            posts = sorted(posts, key = lambda i: int(i['price']))
            return posts
        elif(color == 3):      
            posts = sorted(posts, key = lambda i: parse(i['date_posted']),reverse=True)
            return posts
        elif(color == 4):
            posts = sorted(posts, key = lambda i: parse(i['date_posted']))
            return posts


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
    if(order != "None"):
        filtered_posts = order_filter(list(filtered_posts), int(order))

    filtered_posts = list(filtered_posts)
    return render_template('Products.html', posts=filtered_posts)

@app.route('/quantity_update', methods = ['POST', 'GET'])
def quantity_update():
    if request.method == "POST":
        global brand, name, new_quantity, inst
        print("im accessing")
        new_quantity = str(request.form['new_quantity'])
        brand = str(request.form['brand'])
        name = str(request.form['name'])
        inst = str(request.form['inst'])

        BuyingAgt = BuyingAgent("BuyingAgt@localhost","")
        Buying_start = BuyingAgt.start()
        Buying_start.result()

        Products()
        return str(request.form['new_quantity'])

app.run(debug=True)


