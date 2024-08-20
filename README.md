# Renew my borrowed books

This is a python script that I wrote to renew all the books I borrowed from my college's library.

Every week I needed to check on the library's app if any books passed the due date and click on the "renew" button if it did.

The fact is that I always forgot to do that, so I was paying the library fines everyweek.

*So, instead of spending some minutes setting up reminders on my cellphone, I decided to spend some hours writing this script that checks all my borrowed books and renews them when reached the due date, as every programmer would do!*

Then I setted up as a AWS Lambda script that runs the ``main.handler()`` function and now I will never get fines anymore!

## The algorithm

In summary, 5 steps are required:

1. Login on the college's website
2. Store the acess_token to use in future requests
3. Make the request that list the borrowed books
4. Check the due date of the book,and
5. If it's the due date, make the renew request.

## The API

To discover the URLs and understand the college's API I used my browser DevTools.

### The login

So, logging on my account I saw that the request was:

```
POST /apiapp/login2 HTTP/1.1
Host: portal.multivix.edu.br
```

With a body containing my username and password:

```json
{
	"username": "my-user",
	"password": "my-pass-123"
}
```

### The list of books

Then I clicked on the list of books page and discovered that it was a POST to ``/apiapp/api/biblioteca/listaemprestimorenovavel`` and I got a dict as reponse containing the renewable, non-renewable and the renewed books:
```json
{
	"renovaveis": [
		{
			"codigo": 3751947,
			"ttl_nome": "Física I: mecânica",
			"autor": "YOUNG, Hugh D.",
			"mda_nome": "Livros",
			"dtemprestimo": "2023-09-03T00:00:00",
			"dtdevolucaoestimada": "2023-09-11T00:00:00",
			"renovado": true
		},
		{
			"codigo": 3749846,
			"ttl_nome": "Cálculo",
			"autor": "STEWART, James",
			"mda_nome": "Livros",
			"dtemprestimo": "2023-08-30T00:00:00",
			"dtdevolucaoestimada": "2023-09-06T00:00:00",
			"renovado": true
		}
	],
	"naorenovaveis": [
		{
			"codigo": 0,
			"ttl_nome": "Variáveis complexas e aplicações 3ed., 2013",
			"autor": "ÁVILA, Geraldo",
			"mda_nome": "Livros",
			"dtemprestimo": "2023-09-05T00:00:00",
			"dtdevolucaoestimada": "2023-09-12T00:00:00",
			"renovado": false
		}
	],
	"renovados": [
		{
			"codigo": 0,
			"ttl_nome": "Variáveis complexas e aplicações 3ed., 2013",
			"autor": "ÁVILA, Geraldo",
			"mda_nome": "Livros",
			"dtemprestimo": "2023-09-05T00:00:00",
			"dtdevolucaoestimada": "2023-09-12T00:00:00",
			"renovado": false
		}
	]
}
```

### Renewing the book

Now, having a book to renew, I clicked on the "Renew" button and saw a POST request to ``/apiapp/api/biblioteca/renovaobra`` with only the code book on the body.

## The script

Alright, as I said before, in summary the script needs to login, list the books, check due date and renew. The main process is like the following:
```python
# main.py

def process(self):
	borrowed_books = self.api.list_borrowed_books()

	for book in borrowed_books:
		self.renew_if_is_due_date(book)
```

The first used method list the renewable books:

```python
# api/library_apy

def list_borrowed_books(self):
        path = f'/api/biblioteca/listaemprestimorenovavel'

        try:
            response = self.request('POST', path, headers=headers)

            if response.status_code == 200:
                content = json.loads(response.text)
                borrowed_books = content.get('renovaveis')
                return borrowed_books
        except Exception as e:
            print(e)
```

Then, with the books, the script iterate through the list checking if needs to renew the book:
```python
# main.py

def renew_if_is_due_date(self, book: dict):
	due_date = self.get_due_date(book)

	if self.now > due_date:
		book_code = book['codigo']
		self.api.renew_book(book_code)


def get_due_date(self, book: dict):
	unformatted_due_date = book.get('dtdevolucaoestimada')
	due_date = datetime.strptime(unformatted_due_date, '%Y-%m-%dT%H:%M:%S')
	return due_date
```

And the ``renew_book()`` only makes a POST request with the book code to renew:
```python
# api/library_apy

def renew_book(self, book_code):
	path = f'/api/biblioteca/renovaobra'

	body = {
		'codigo': book_code
	}

	try:
		response = self.request('POST', path, body=body)
		return response
	except Exception as e:
		print(e)
```

Here are only the main steps of the code and you can check more deeply on the repo.

## The hosting

To host I used a AWS Lambda function with a trigger everyday at 00:10am, since the renewal dates are always at every midnight.
Looking at the logs I can verify that everything is running correctly:
![image](https://github.com/user-attachments/assets/d62bf63a-233e-4bdf-95d5-772c971ee4c8)

