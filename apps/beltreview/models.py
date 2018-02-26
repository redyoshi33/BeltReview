# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
name_regex = re.compile(r'^[a-zA-Z]+$')


class usersmanager(models.Manager):
	def basic_validator_register(self, postData):
		errors = {}
		if len(postData['name']) == 0:
			errors['blname'] = "Can't leave the name fields empty"		
		elif len(postData['name']) < 2:
			errors['names'] = 'Name must be at least 2 characters long'
		elif not name_regex.match(postData['name']):
			errors['vnames'] = 'Please put a valid first name'
		elif len(postData['email']) < 1:
			errors['blemail'] = "Can't leave the email field empty"
		elif not email_regex.match(postData['email']):
			errors['vlemail'] = 'Please put a valid email'
		elif User.objects.filter(email=(postData['email']).lower()).exists():
			errors['alreadyreg'] = "This email is already registered"
		elif len(postData['pword']) < 1:
			errors['blpword'] = "Must include password"
		elif len(postData['pword']) < 8:
			errors['pword'] = "Password needs to be at least 8 characters long"
		elif postData['pword'] != postData['cpword']:
			errors['cpword'] = 'Passwords do not match'
		else:
			password = bcrypt.hashpw(postData['pword'].encode(), bcrypt.gensalt())
			user = User.objects.create(name=postData['name'], alias=postData['alias'], email=(postData['email']).lower(), pword=password)
			errors['user'] = user
		return errors
		

	def basic_validator_login(self, postData):
		errors={}
		if not User.objects.filter(email=(postData['email']).lower()).exists():
			errors['fail'] = 'Email/password input incorrect'
		elif not bcrypt.checkpw(postData['pword'].encode(), User.objects.get(email=(postData['email']).lower()).pword.encode()):
			errors['fail'] = 'Email/password input incorrect'
		else:
			user = User.objects.get(email=(postData['email']).lower())
			errors['user'] = user
		return errors

class booksmanager(models.Manager):
	def validate_books(self,postData,session):
		user = User.objects.get(id=session)
		errors={}
		if len(postData['title']) == 0:
			errors['title'] = "Can't leave the title field empty"		
		if len(postData['oldauthor']) == 0 and len(postData['newauthor']) == 0:
			errors['author'] = "There is no author"
		if len(postData['review']) == 0:
			errors['review'] = "Can't leave the review field empty"
		else:
			if len(postData['newauthor']) > 0:
				if Book.objects.filter(title=postData['title']).filter(author=postData['newauthor']).exists():
					book = Book.objects.get(title=postData['title'])
					errors['book'] = book
					Review.objects.create(content=postData['review'], rating=postData['rating'], reviewer=user, book=book)
				else:
					book = Book.objects.create(title=postData['title'], author=postData['newauthor'], uploader=user)
					errors['book'] = book
					Review.objects.create(content=postData['review'], rating=postData['rating'], reviewer=user, book=book)
			else:
				if Book.objects.filter(title=postData['title']).filter(author=postData['oldauthor']).exists():
					book = Book.objects.get(title=postData['title'])
					errors['book'] = book
					Review.objects.create(content=postData['review'], rating=postData['rating'], reviewer=user, book=book)
				else:
					book = Book.objects.create(title=postData['title'], author=postData['oldauthor'], uploader=user)
					errors['book'] = book
					Review.objects.create(content=postData['review'], rating=postData['rating'], reviewer=user, book=book)
		return errors

class reviewsmanager(models.Manager):
	def validate_reviews(self,postData,session, bid):
		user = User.objects.get(id=session)
		book = Book.objects.get(id=bid)
		errors={}
		if len(postData['review']) == 0:
			errors['empreview'] = "Can't submit review without anything"
		else:
			review = Review.objects.create(content=postData['review'], rating=postData['rating'], reviewer=user, book=book)
			errors['review'] = review
		return errors
	def delete_review(self, rid):
		review = Review.objects.get(id=rid)
		bookid = review.book.id
		review.delete()
		return bookid

class User(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	pword = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = usersmanager()

class Book(models.Model):
	title = models.CharField(max_length=255)
	author = models.CharField(max_length=255)
	uploader = models.ForeignKey(User, related_name='books_uploaded')
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = booksmanager()

class Review(models.Model):
	content = models.TextField()
	rating = models.IntegerField()
	reviewer = models.ForeignKey(User, related_name='reviews_uploaded')
	book = models.ForeignKey(Book, related_name='reviews')
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = reviewsmanager()