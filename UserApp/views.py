from django.shortcuts import render,redirect
from AdminApp .models import Category,Product,UserInformation,PaymentMaster
from UserApp.models import MyCart,OrderMaster
from datetime import datetime
from django.contrib import messages
# Create your views here
def homepage(request):
  # Fetch all records from category table
    cats = Category.objects.all()
    products = Product.objects.all()
    return render(request,"homepage.html",{"cats":cats,"products":products})

def login(request):
    cats = Category.objects.all()
    if(request.method == "GET"):
        return render(request,"login.html",{"cats":cats})
    else:
        uname = request.POST["uname"]
        password = request.POST["password"]
        try:
            user = UserInformation.objects.get(uname=uname,password=password)
            messages.success(request,'Login successful')
        except:
            messages.success(request,'Invalid Login')
            return redirect(login)
        else:
            #create the session
            request.session["uname"] = uname
            return redirect(homepage)

def signup(request):
    cats = Category.objects.all()
    if(request.method == "GET"):
        return render(request,"signup.html",{"cats":cats})
    else:
        uname = request.POST["uname"]
        password = request.POST["password"]
        email = request.POST["email"]
        user = UserInformation(uname,password,email)
        user.save()
        return redirect(login)

def signout(request):
    request.session.clear()
    return redirect(homepage)

def ShowProducts(request,id):
    #get method returns single object
    id = Category.objects.get(id=id)
    #filter method returns multiple objects
    products = Product.objects.filter(cat = id)
    cats = Category.objects.all()
    return render(request,"homepage.html",{"cats":cats,"products":products})

def ViewDetails(request,id):
    product = Product.objects.get(id=id)
    cats = Category.objects.all()
    return render(request,"ViewDetails.html",{"product":product,"cats":cats})

def addToCart(request):
    if(request.method == "POST"):
        if("uname" in request.session):
            #Add to cart
            productid = request.POST["productid"]
            user = request.session["uname"]
            qty = request.POST["qty"]
            product = Product.objects.get(id=productid)
            user = UserInformation.objects.get(uname = user)
            #check for duplicate entry
            try:
                cart = MyCart.objects.get(product=product,user=user)
            except:
                cart = MyCart()
                cart.user = user
                cart.product = product
                cart.qty = qty
                cart.save()
            else:
                pass
            return redirect(homepage)
        else:
            return redirect(login)

def ShowAllCartItems(request):
    cats = Category.objects.all()
    uname = request.session["uname"]
    user = UserInformation.objects.get(uname=uname)
    if(request.method == "GET"):
        cartitems = MyCart.objects.filter(user=user)
        total = 0
        for item in cartitems:
            total += item.qty*item.product.price
        request.session["total"]=total
        return render(request,"ShowAllCartItems.html",{"items":cartitems,"cats":cats})
    else:
        id = request.POST["productid"]
        product = Product.objects.get(id=id)
        item = MyCart.objects.get(user=user,product=product)
        qty = request.POST["qty"]
        item.qty = qty
        item.save() #update
        return redirect(ShowAllCartItems)

def MakePayment(request):
    if(request.method == "GET"):
        return render(request,"MakePayment.html",{})
    else:
        cardno = request.POST["cardno"]
        cvv = request.POST["cvv"]
        expiry = request.POST["expiry"]
        try:
            buyer = PaymentMaster.objects.get(cardno=cardno,cvv=cvv,expiry=expiry)
        except:
            return redirect(MakePayment)
        else:
            #its a match
            owner = PaymentMaster.objects.get(cardno='111',cvv='111',expiry='12/2025')
            owner.balance += request.session["total"]
            buyer.balance -= request.session["total"]
            owner.save()
            buyer.save()
            #Delete all items from cart
            uname = request.session["uname"]
            user = UserInformation.objects.get(uname=uname)
            order = OrderMaster()
            order.user = user
            order.amount = request.session["total"]
            #order.dateOfOrder= datetime.now()
            #Fetch all cart items for that user
            details = ""
            items = MyCart.objects.filter(user=user)
            for item in items:
                details += (item.product.pname) +","
                item.delete()
            order.details = details
            order.save()

            return redirect(homepage)

def removeItem(request):
    uname = request.session["uname"]
    user = UserInformation.objects.get(uname=uname)
    id = request.POST["productid"]
    product = Product.objects.get(id=id)
    item = MyCart.objects.get(user=user,product=product)
    item.delete()
    return redirect(ShowAllCartItems)
