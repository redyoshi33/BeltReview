# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages

def index(request):
	if 'uid' not in request.session:
		request.session['uid'] = 0
	return render(request, 'beltapp/index.html')

def regis(request):
	if request.method == 'POST':
		errors = User.objects.basic_validator_register(request.POST)
		if 'user' in errors:
			request.session['uid'] = errors['user'].id
			return redirect('/books')
		else:
			for tag, error in errors.iteritems():
				messages.error(request, error, extra_tags=tag)
			return redirect('/')

def login(request):
	if request.method == 'POST':
		errors = User.objects.basic_validator_login(request.POST)
		if 'user' in errors:
			request.session['uid'] = errors['user'].id
			return redirect('/books')
		else:
			for tag, error in errors.iteritems():
				messages.error(request, error, extra_tags=tag)
			return redirect('/')

def bookhome(request):
	context = {
		"user": User.objects.get(id=request.session['uid']),
		'books': Book.objects.all(),
		'reviews': Review.objects.all().order_by('-created_at')[:3],
	}
	return render(request, 'beltapp/bookshome.html', context)

def addbook(request):
	context = {
		'authors': Book.objects.values_list('author', flat=True).distinct()
	}
	return render(request, 'beltapp/addbook.html', context)

def submit(request):
	if request.method == 'POST':
		errors = Book.objects.validate_books(request.POST, request.session['uid'])
		if 'book' in errors:
			bid = errors['book'].id
			return redirect('/books/'+str(bid))
		else:
			for tag, error in errors.iteritems():
				messages.error(request, error, extra_tags=tag)
			return redirect('/books/add')

def reviews(request, id):
	if request.method == 'POST':
		errors = Review.objects.validate_reviews(request.POST, request.session['uid'], id)
		if 'review' in errors:
			return redirect('/books/'+str(id))
		else:
			for tag, error in errors.iteritems():
				messages.error(request, error, extra_tags=tag)
			return redirect('/books/'+str(id))

def delete(request, id):
	bookid = Review.objects.delete_review(id)
	return redirect('/books/'+str(bookid))

def showbook(request, id):
	context = {
		'reviews': Review.objects.filter(book=id),
		'books': Book.objects.get(id=id),
		'uid': request.session['uid'],
	}
	return render(request, 'beltapp/bookshow.html', context)

def users(request, id):
	review = Review.objects.filter(reviewer=id)
	context ={
		'user': User.objects.get(id=id),
		'reviews': review,
		'count': review.count()
	}
	return render(request, 'beltapp/users.html', context)

def logout(request):
	request.session.clear()
	return redirect('/')


