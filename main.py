import json
import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.carousel import Carousel
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.core.window import Window


# klasa książki
class Book():
	def __init__(self, title = 'Brak tytułu', author = 'Nieznany', status = 'Nie', isbn = '0000000000000'):
		self.title = str(title).capitalize()
		self.author = str(author)
		self.status = str(status).capitalize()
		self.isbn = str(isbn)

	def edit_book(self, title, author, status, isbn):
		self.title = str(title).capitalize()
		self.author = str(author)
		self.status = str(status).capitalize()
		self.isbn = str(isbn)


class MyGrid(Widget):
	global books_list, showed_books

	def load_books(self):
		carousel_kv = self.ids.carousel_kv
		write_books(carousel_kv, books_list, showed_books)

	def add_book(self):
		show = Add_book_popup()
		carousel_kv = self.ids.carousel_kv
		show.show_popup(show, carousel_kv)

	def remove_book(self):
		show = remove_book_popup()
		carousel_kv = self.ids.carousel_kv
		show.show_popup(show, carousel_kv)

	def edit_book(self):
		show = Edit_book_popup()
		carousel_kv = self.ids.carousel_kv
		show.show_popup(show, carousel_kv)

	def search_book(self):
		show = Search_book_popup()
		carousel_kv = self.ids.carousel_kv
		show.show_popup(show, carousel_kv)


class Add_book_popup(FloatLayout):
	global books_list, showed_books
	new_title = ObjectProperty(None)
	new_date = ObjectProperty(None)
	new_status = ObjectProperty(None)
	new_isbn = ObjectProperty(None)

	def show_popup(self,me, passed_carousel):
		self.popupWindow = Popup(title='Dodaj książkę', content=me, size_hint=(0.8,0.6))
		self.popupWindow.open()
		self.carousel = passed_carousel
		
	def add_book(self):
		books_list.insert(0,Book(self.new_title.text, self.new_date.text, self.new_status.text, self.new_isbn.text))  # wciska książkę na początek listy
		save_data(books_list)  # zapisuje książki i resetuje pokazywanie książek
		showed_books = range(0,len(books_list))
		write_books(self.carousel, books_list, showed_books)
		self.popupWindow.dismiss()


class remove_book_popup(FloatLayout):
	global books_list, showed_books
	book_number = ObjectProperty(None)

	def show_popup(self,me, passed_carousel):
		self.popupWindow = Popup(title='Usuń książkę', content=me, size_hint=(0.8,0.6))
		self.popupWindow.open()
		self.carousel = passed_carousel


	def remove_book(self):
		idx_delete = int(self.book_number.text)
		if idx_delete in range(1,len(books_list)+1):
			books_list.pop(idx_delete-1)  # usuwa książkę o podanym indeksie
			save_data(books_list)
			showed_books = range(0,len(books_list))
		else: 
			print("Nie ma takiego numeru")
		write_books(self.carousel, books_list, showed_books)
		self.popupWindow.dismiss()


class Edit_book_popup(FloatLayout):
	global books_list, showed_books
	book_number = ObjectProperty(None)
	new_title = ObjectProperty(None)
	new_date = ObjectProperty(None)
	new_status = ObjectProperty(None)
	new_isbn = ObjectProperty(None)

	def show_popup(self, me, passed_carousel):
		self.popupWindow = Popup(title='Edytuj książkę', content=me, size_hint=(0.8,0.6))
		self.popupWindow.open()
		self.carousel = passed_carousel

	def edit_book(self):
		idx_edit = int(self.book_number.text)
		if idx_edit in range(1,len(books_list)+1):
			books_list[idx_edit-1].edit_book(self.new_title.text, self.new_date.text, self.new_status.text, self.new_isbn.text)  # edytuje książkę o podanym indeksie
			save_data(books_list)
			showed_books = range(0,len(books_list))
		else: 
			print("Nie ma takiego numeru")
		write_books(self.carousel, books_list, showed_books)
		self.popupWindow.dismiss()


class Search_book_popup(FloatLayout):
	global books_list, showed_books
	search_phrase = ObjectProperty(None)

	def show_popup(self, me, passed_carousel):
		self.popupWindow = Popup(title='Szukaj książki', content=me, size_hint=(0.8,0.6))
		self.popupWindow.open()
		self.carousel = passed_carousel

	def search_book(self):
		searched_phrase = self.searched_phrase.text
		if len(searched_phrase) <= 0:
			print("Zresetowano wyszukiwanie")  # jeśli nic nie wpiszesz to wyszukiwanie się zresetuje
			showed_books = range(0,len(books_list))
			
		showed_books = search_phrase(books_list, searched_phrase)  # wyszukiwanie książek i zapisywanie ich indeksów
		write_books(self.carousel, books_list, showed_books)
		self.popupWindow.dismiss()

# klasa odpalająca apke
class Libteka(App):
	def build(self):
		Window.clearcolor = (0.1,0.1,0.1,1)
		return MyGrid()


# pobranie danych z pliku jako lista słowników
def get_data(path):
	data = []
	with open(path,'r') as f:
		for x in json.load(f)['books']:
			data.append(x)
	return data

# zapisuje dane z listy słowników do pliku json
def save_data(passed_books_list):
	with open('data_json.json', 'w') as f:
		json.dump(object_to_dict(passed_books_list), f, indent = 5)

# utworzenie listy obiektów klasy książka z danych z listy 
def dict_to_object(passed_data):
	books_list = []
	for i in passed_data:
		books_list.append(Book(i['title'], i['author'], i['status'], i['isbn']))
	return books_list

# tworzenie listy słowników z obiektów
def object_to_dict(passed_books_list):
	new_data_json = []
	for i in passed_books_list:
		slownik_temp = {'title':i.title, 'author': i.author, 'status': i.status, 'isbn': i.isbn}
		new_data_json.append(slownik_temp)
	x = {'books': new_data_json}
	return x

# Funkcja wyszykuje w liście obiektów podane teksty i zwraca indeksy występowania ich w liście
def search_phrase(passed_list, search_phrase=''):
	indxes = []
	for idx, item in enumerate(passed_list):
		title = item.title
		if title.lower().find(search_phrase.lower()) != -1:
			indxes.append(idx)
	return indxes

# funckcja wypisująca scrolla z książkami
def write_books(carousel, passed_books_list, passed_showed_books):
	carousel.clear_widgets()
	content_list = []
	x = 1
	content_list.append(GridLayout(cols=1))
	for i in passed_showed_books:
		new_label = GridLayout(cols = 1)
		new_label.add_widget(Button(text=('Nr.' + str(i+1) + '\nTytuł: ' + '"' + passed_books_list[i].title + '"'), disabled = True, halign="center"))

		info = GridLayout(cols = 3)
		info.add_widget(Button(text = ('Autor:\n' + passed_books_list[i].author), disabled = True, halign="center"))
		info.add_widget(Button(text = ('Status\nprzeczytania:\n' + passed_books_list[i].status), disabled = True, halign="center"))
		info.add_widget(Button(text = ('ISBN:\n' + passed_books_list[i].isbn), disabled = True, halign="center"))
		new_label.add_widget(info)

		content_list[-1].add_widget(new_label)
		if x >= 4:
			content_list.append(GridLayout(cols=1))
			x = 1
			continue
		x += 1
	if x <= 4:
		while(x <= 4):
			content_list[-1].add_widget(Label())
			x += 1
	if len(passed_showed_books)%4 == 0 and int(len(passed_showed_books)/4) != len(content_list):
		content_list.pop(-1)
	for x in content_list:
		carousel.add_widget(x)


if __name__ == "__main__":
	try:
		data_json = get_data('data_json.json')
		books_list = dict_to_object(data_json)
		
	except:
		books_list = []
		books_list.append(Book('Brak tytułu','Nieznany','Nie','0000000000000'))

	# pokazywane książki, indeksy książek z listy które mają być pokazane
	showed_books = range(0,len(books_list))

	Libteka().run()
