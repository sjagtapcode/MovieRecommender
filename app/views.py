from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from app.models import Movies,Lists
from django.core.paginator import Paginator
from django.views.generic import ListView


def index(request):
	return render(request,'index.html')

def listallmovies(request):
	movies_list = Movies.objects.all();
	paginator = Paginator(movies_list, 20)
	page_number = request.GET.get('page');
	print("------------------------")
	page_obj = paginator.get_page(page_number)
	last_page_number = int(movies_list.count()/20)
	context={'movies':page_obj,'page_number':page_number,'last_page_number':last_page_number}
	if(page_obj.has_previous()):
		context['prev_page_number']=page_obj.previous_page_number()
	if(page_obj.has_next()):
		context['next_page_number']=page_obj.next_page_number()
	return render(request,"movies/page.html",context)

def singlemovie(request,id):
	movie = Movies.objects.get(mid__exact=id)
	playlists = Lists.objects.order_by('lid');
	context={'movie':movie,'playlists':playlists};
	return render(request,"movies/single_movie.html",context)

def createlist(request):
	if (request.method == "GET"):
		movies_list = Movies.objects.all();
		return render(request,"watchlist/createlist.html",{'movies':movies_list})

	elif (request.method == "POST"):
		mids=request.POST.getlist('checklist')
		movies_list = Movies.objects.filter(mid__in=mids);
		return render(request,"watchlist/listcreated.html",{'movies':movies_list})

def addtowatchlist(request):
	if (request.GET.get('mid')):
		mid = int(request.GET.get('mid'))
		lid = int(request.GET.get('lid'))
		print("--------------")
		w=Lists.objects.filter(lid__exact=lid)
		x=w[0].mylist
		if(x):
			print(x)
		else:
			x=[]
		setx = set(x)
		if mid in setx:
			print("already exists")
		else:
			x.append(mid)
			Lists.objects.filter(lid__exact=lid).update(mylist=x)
		return HttpResponseRedirect("singlemovie/"+str(mid))
#		return HttpResponseRedirect(request.path_info)
	else:
		return render(request,"index.html")

