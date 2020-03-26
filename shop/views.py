from django.shortcuts import render
from .models import Product,Contact,Orders,OrderUpdate
from math import ceil
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .PayTm import Checksum

merchant_key = 'cqnATyGBO96F2i3Z';


# Create your views here.
def index(request):
    # products = Product.objects.all()
    # n = len(products)
    # nSlides = n//4 * ceil((n/4)-(n//4))
    # parms = {"no_of_slides":nSlides, "range":range(1,nSlides), "product" : products}
    # allProds = [[products,range(1,nSlides),nSlides],
    #             [products, range(1,nSlides), nSlides]]
    allProds=[]
    catprods = Product.objects.values('category','id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 * ceil((n / 4) - (n // 4))
        allProds.append([prod,range(1,nSlides),nSlides])
    parms={'allProds':allProds}
    return  render(request,"shop/index.html",parms)

def searchMatch(query,item):
    # return true only query item match
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query,item)]
        n = len(prod)
        nSlides = n // 4 * ceil((n / 4) - (n // 4))
        if len(prod)!=0:
            allProds.append([prod, range(1, nSlides), nSlides])
    parms = {'allProds': allProds,'msg':''}
    if len(allProds)==0 or len(query)<4:
        parms = {'msg': 'please make sure to enter relevant search query'}
    return  render(request,"shop/search.html",parms)

def about(request):
    return  render(request,"shop/about.html")

def contact(request):
    thank = False
    if request.method=="POST":
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        mobile = request.POST.get('mobile','')
        dec = request.POST.get('message','')
        contact = Contact(name=name,email=email,mobile=mobile,desc=dec)
        contact.save()
        thank = True
    return render(request,"shop/contact.html",{'thank':thank})


def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        # return HttpResponse(f"{orderId} and {eamil}")
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates=[]
                for item in update:
                    updates.append({'text': item.update_desc,'time': item.timestamp})
                    response = json.dumps({"status":"success","updates":updates,"itemJson":order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')
    return render(request, "shop/tracker.html")

# def tracker(request):
#     if request.method == "POST":
#         orderId = request.POST.get('order_id', '')
#         email = request.POST.get('email', '')
#         try:
#             order = Orders.objects.filter(order_id=orderId,email=email)
#             if len(order)>0:
#                 update = OrderUpdate.objects.filter(order_id=orderId)
#                 updates=[]
#                 for item in update:
#                     updates.append({'text': item.update_desc,'time': item.timestamp})
#                     response = json.dumps(updates)
#                     return HttpResponse(response)
#             else:
#                 pass
#     return render(request, "shop/tracker.html")

def checkout(request):
        if request.method == "POST":
            itemjson = request.POST.get('itemJson', '')
            amount = request.POST.get('amount', '')
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            address = request.POST.get('address', '')      
            address2 = request.POST.get('address', '')      
            city = request.POST.get('city', '')      
            state = request.POST.get('state', '')      
            phone = request.POST.get('phone', '')      
            zip = request.POST.get('zip', '')      
            order = Orders(items_json=itemjson, name=name, email=email, address=address,
                           address2=address2, city=city, state=state, phone_no=phone, zip_code=zip,Amount=amount)
            order.save()
            update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
            update.save()
            thank = True
            id = order.order_id
            # return render(request, "shop/checkout.html",{'thank':thank,'id':id})
            # request paytm  to transfar the amount
            param_dict = {
                'MID': 'jruKkn84982520926012',
                'ORDER_ID': str(order.order_id),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http:/127.0.0.1:8000/shop/handlerequest/',
            }
            param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, merchant_key)
            return render(request, "shop/paytm.html",{'param_dict':param_dict})
        return render(request, "shop/checkout.html")

@csrf_exempt
def handlerequest(request):
    # paytm will send post request here
    form = request.POST
    response_dict ={}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    verify = Checksum.verify_checksum(response_dict,merchant_key,checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because',response_dict['RESPMSC'])
    return render(request,'shop/paymentstatus.html',{"response":response_dict})

def productView(request,myid):
    product = Product.objects.filter(id=myid)
    return  render(request,"shop/productView.html",{'product':product[0]})

