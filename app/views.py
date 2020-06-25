# from django.shortcuts import render
# from django.http import HttpResponse
# from django.http import HttpResponseRedirect
# from app.models import Movies,Lists
# from django.core.paginator import Paginator
# from django.views.generic import ListView
#
#
# def index(request):
# 	return render(request,'index.html')
#
#
# def listallmovies(request):
# 	movies_list = Movies.objects.all();
# 	paginator = Paginator(movies_list, 20)
# 	page_number = request.GET.get('page');
# 	print("------------------------")
# 	page_obj = paginator.get_page(page_number)
# 	last_page_number = int(movies_list.count()/20)
# 	context={'movies':page_obj,'page_number':page_number,'last_page_number':last_page_number}
# 	if(page_obj.has_previous()):
# 		context['prev_page_number']=page_obj.previous_page_number()
# 	if(page_obj.has_next()):
# 		context['next_page_number']=page_obj.next_page_number()
# 	return render(request,"movies/page.html",context)
#
#
# def singlemovie(request,id):
# 	movie = Movies.objects.get(mid__exact=id)
# 	playlists = Lists.objects.order_by('lid');
# 	context = {'movie':movie,'playlists':playlists};
# 	return render(request,"movies/single_movie.html",context)
#
#
# def singlelist(request,lid):
# 	listx = Lists.objects.get(lid__exact=lid)
# 	context = { list : listx }
# 	return render(request,"movies/playlists.html",context)
#
#
# # def createlist(request):
# # 	if (request.method == "GET"):
# # 		movies_list = Movies.objects.all();
# # 		return render(request,"watchlist/createlist.html",{'movies':movies_list})
# #
# # 	elif (request.method == "POST"):
# # 		mids=request.POST.getlist('checklist')
# # 		movies_list = Movies.objects.filter(mid__in=mids);
# # 		return render(request,"watchlist/listcreated.html",{'movies':movies_list})
#
#
# def createmyownlist(request):
# 	mids = request.GET.get('mid')
# 	listname = request.GET.get('listname')
# 	print("-----------------------")
# 	print(listname)
# 	print(mids)
# 	cnt = Lists.objects.count()
# 	Lists.objects.create(name=listname,lid=cnt+1,mylist=list(mids))
# 	return HttpResponseRedirect("singlemovie/"+str(mids))
#
# def addtowatchlist(request):
# 	if (request.GET.get('mid')):
# 		mid = int(request.GET.get('mid'))
# 		lid = int(request.GET.get('lid'))
# 		print("--------------")
# 		w=Lists.objects.filter(lid__exact=lid)
# 		x=w[0].mylist
# 		if(x):
# 			print(x)
# 		else:
# 			x=[]
# 		setx = set(x)
# 		if mid in setx:
# 			print("already exists")
# 		else:
# 			x.append(mid)
# 			Lists.objects.filter(lid__exact=lid).update(mylist=x)
# 		return HttpResponseRedirect("singlemovie/"+str(mid))
# #		return HttpResponseRedirect(request.path_info)
# 	else:
# 		return render(request,"index.html")
#
#














from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from app.models import Movies,Lists
from django.core.paginator import Paginator
from django.views.generic import ListView

import app.schema
import graphene

schema = graphene.Schema(query=app.schema.Query,mutation=app.schema.Mutation)


def index(request):
	return render(request,'index.html')


def listallmovies(request):
	page_number=request.GET.get('page')
	result = schema.execute(
		'''
		{
			allMovies(page:'''+str(page_number)+'''){
				objects{
				mid,
				title
				}
			}
		}
		'''
	)
	context={"movies":result.data["allMovies"][0]["objects"]}

	return render(request,"movies/page.html",context)


def singlemovie(request,id):
	movie = schema.execute(
		'''
		{
		  singleMovie(id:'''+str(id)+'''){
			mid
			voteCount
			voteAverage
			releaseDate
			language
			title
			adult
			popularity
			posterPath
			genreIds
			overview
		  }
		}
		'''
	)
	playlists = schema.execute(
		'''
		{
		  allLists{
			lid,
			name
		  }
		}
		'''
	)
	context = {'movie':movie.data['singleMovie'][0],'playlists':playlists.data['allLists']}
	return render(request,"movies/single_movie.html",context)


def singleplaylist(request,id):
	listx = schema.execute(
		'''
		{
			singleList(lid:'''+str(id)+'''){
				lid
				name
				mylist
			}
		}
		'''
	)
	context = { 'list' : listx.data['singleList'][0] , 'ply':listx.data['singleList'][0]['mylist']}
	return render(request,"watchlist/single_playlist.html",context)


def createmyownlist(request):
	listname = request.GET.get('listname')
	mid = request.GET.get('mid')
	result = schema.execute(
		'''
		mutation{
			createList(name:"'''+str(listname)+'''"){
	    	createListErrors
	    	lid
	  		}
		}
		'''
	)
	resultx = schema.execute(
		'''
		mutation{
			addToList(lid:'''+str(result.data['createList']['lid'])+''',mid:'''+str(mid)+'''){
				addToListErrors
			}
		}
		'''
	)
	return HttpResponseRedirect("singlemovie/"+str(mid))


def addtowatchlist(request):
	if (request.GET.get('mid')):
		mid = int(request.GET.get('mid'))
		lid = int(request.GET.get('lid'))
		result = schema.execute(
			'''
			mutation{
				addToList(lid:'''+str(lid)+''',mid:'''+str(mid)+'''){
				addToListErrors
		  		}
			}
			'''
		)
		return HttpResponseRedirect("singlemovie/"+str(mid))
	else:
		return render(request,"index.html")


def listalllist(request):
	playlists = schema.execute(
	'''
		{
		  allLists{
			lid,
			name
		  }
		}
	'''
	)
	context = {'playlists':playlists.data['allLists']}
	return render(request,"watchlist/playlists.html",context)


