from django.shortcuts import render
from .models import OrderItem, Transaction
from .forms import OrderCreateForm
from cart.cart import Cart
import sys
import operator
from itertools import chain, combinations
from collections import defaultdict
from django.shortcuts import render, get_object_or_404, render_to_response
from catalog.models import City, Country, Hotel,  Tour
from catalog.models import Point
from orders.models import Transaction



def subsets(arr):

    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])


def returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet):

        """вычисляет поддержку элементов в itemSet и возвращает подмножество itemSet, каждый из
        элементов которого удовлетворяет минимальной поддержке"""
        _itemSet = set()
        localSet = defaultdict(int)

        for item in itemSet:
                for transaction in transactionList:
                        if item.issubset(transaction):
                                freqSet[item] += 1
                                localSet[item] += 1

        for item, count in localSet.items():
                support = float(count)/len(transactionList)

                if support >= minSupport:
                        _itemSet.add(item)

        return _itemSet


def joinSet(itemSet, length):
        """Объединение i-элементных наборов длины к, преданной из функции"""
        return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])


def getItemSetTransactionList(data_iterator):
    """Получение множества транзакций и списка транзакций"""
    transactionList = list()
    itemSet = set()
    for record in data_iterator:
        transaction = frozenset(record)
        transactionList.append(transaction)
        for item in transaction:
            itemSet.add(frozenset([item]))              # Generate 1-itemSets
    return itemSet, transactionList


def runApriori(data_iter, minSupport=0.01, minConfidence=0.4):
    """

     - items (tuple, support)
     - rules ((pretuple, posttuple), confidence)
    """
    itemSet, transactionList = getItemSetTransactionList(data_iter)

    freqSet = defaultdict(int)
    largeSet = dict()
    # Словарь хранить (key=n-itemSets,value=support)
    # удовлетворяет minSupport

    oneCSet = returnItemsWithMinSupport(itemSet,
                                        transactionList,
                                        minSupport,
                                        freqSet)

    currentLSet = oneCSet
    k = 2
    while(currentLSet != set([])):
        largeSet[k-1] = currentLSet
        """объединить в k-элементные кандидаты (k-1)-элементные частые наборы."""
        """Остальные наборы затем объединяются для создания наборов предметов с k элементами"""
        currentLSet = joinSet(currentLSet, k)
        currentCSet = returnItemsWithMinSupport(currentLSet,
                                                transactionList,
                                                minSupport,
                                                freqSet)
        currentLSet = currentCSet
        k = k + 1

    def getSupport(item):
            """возвращает поддержку для каждого айтем"""
            return float(freqSet[item])/len(transactionList)

    toRetItems = []
    for key, value in largeSet.items():
        toRetItems.extend([(tuple(item), getSupport(item))
                           for item in value])

    toRetRules = []
    for key, value in list(largeSet.items())[1:]:
        for item in value:
            _subsets = map(frozenset, [x for x in subsets(item)])
            for element in _subsets:
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = getSupport(item)/getSupport(element)
                    if confidence >= minConfidence:
                        toRetRules.append(((tuple(element), tuple(remain)),
                                           confidence))
    return toRetItems, toRetRules


def printResults(items, rules):

    for item, support in sorted(items, key=operator.itemgetter(1)):
        print ("item: %s , %.3f" % (str(item), support))
    print ("\n------------------------ RULES:")
    for rule, confidence in sorted(rules, key=operator.itemgetter(1)):
        pre, post = rule
        print ("Rule: %s ==> %s , %.3f" % (str(pre), str(post), confidence))

def listrules(rules, tourid):
    listrulesf=[]
    for rule, confidence in sorted(rules, key=operator.itemgetter(1)):
          pre, post = rule
          if pre[0]==str(tourid):
              v = post[0]
              listrulesf.append(v)
              print(v)
    return listrulesf

def aprioriDB(tourid):
    InFile = dataFromDB()
    items, rules = runApriori(InFile, 0.01, 0.4)
    printResults(items, rules)
    listofas = listrules(rules, tourid)
    return listofas

def dataFromDB():

   file_iter = Transaction.objects.all()
   for line in file_iter:
       q = line.col
       l = str(q)
       l=l.replace("[", "").replace("]", "").replace("'", "")
       print(l)
       print(type(l))
       l = l.strip().rstrip(',')
       record = frozenset(l.split(','))
       yield record

def OrderCreate(request):
    cart = Cart(request)
    listrules = []
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, tour=item['tour'],
                                         price=item['price'],
                                         quantity=item['quantity'])
                idt = item['tour'].id
                l =aprioriDB(idt)
                listrules.append(l)

            cart.clear()
            tours = Tour.objects.all()
            points = Point.objects.all()
            listint = []
            for elem in listrules:
                for el in elem:
                    if int(el) not in listint:
                        listint.append(int(el))
            print(listint)


            return render(request, 'orders/created.html', {'order': order, 'tours': tours, 'points': points, 'listofr': listint})

    form = OrderCreateForm()
    return render(request, 'orders/create.html', {'cart': cart,
                                                      'form': form})



