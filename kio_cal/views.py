from annoying.decorators import render_to
from django.http import Http404
from django.shortcuts import get_object_or_404
from models import Release, Article

@render_to('kio_cal/calendar.html')
def frontpage(request):
    try:
        release = Release.objects.public()[0]
        return {'release':lambda:release}
    except IndexError:
        return {'release':None}

@render_to('kio_cal/calendar.html')
def release(request,pk):
    return {'release':Release.objects.get(pk=pk)}

@render_to('kio_cal/article.html')
def article(request,pk):
    return {'article':Article.objects.get(pk=pk)}

@render_to('kio_cal/calendar.html')
def release_by_date(request,year,month,count=0):
    #Magic cus of specific releases naming
#    month = int(month)
#    year = int(year)
#
#    month -= 1
#    if month < 1:
#        month = 12
#        year -=1

    skiper = 0
    for release in Release.objects.public().filter(publication_ts__year=year,
                                          publication_ts__month=month):
        #roll to wanted release
        if count and skiper < int(count):
            skiper += 1
            continue

        return {'release':release}

    raise Http404