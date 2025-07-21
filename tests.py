import pytest

from main import BooksCollector


class TestBooksCollector:

    @pytest.fixture(autouse=True)
    def collector(self):
        self.collector = BooksCollector()
        return self.collector

    def generate_book_list(
        self,
        book_count_for_genre=5,
        excluded_genres=[],
    ):
        for genre in [
            i for i in (*self.collector.genre, '') if i not in excluded_genres
        ]:
            for i in range(book_count_for_genre):
                self.collector.books_genre[
                    f'Книга №{i + 1} жанра {genre[:20]}'
                ] = genre

    def test_add_new_book_add_two_books(self):
        self.collector.add_new_book('Гордость и предубеждение и зомби')
        self.collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        assert len(self.collector.get_books_genre()) == 2

    @pytest.mark.parametrize(
        'name',
        ['', 'Название книги с длиной более чем 40 символов'],
    )
    def test_add_new_book_wrong_name_length_not_added(self, name):
        self.collector.add_new_book(name)

        assert len(self.collector.get_books_genre()) == 0

    def test_add_new_book_already_added_not_added_twise(self):
        self.collector.add_new_book('Название книги')
        self.collector.add_new_book('Название книги')

        assert len(self.collector.get_books_genre()) == 1

    @pytest.mark.parametrize('genre', BooksCollector().genre)
    def test_set_book_genre_genre_in_list_genre_is_set(self, genre):
        name = 'Название книги'
        self.collector.add_new_book(name)
        self.collector.set_book_genre(name, genre)

        assert self.collector.books_genre[name] == genre

    def test_set_book_genre_genre_not_in_list_genre_empty(self):
        name = 'Название книги'
        self.collector.add_new_book(name)
        self.collector.set_book_genre(name, 'Неизвестный жанр')

        assert self.collector.books_genre[name] == ''

    @pytest.mark.skipif(
        len(BooksCollector().genre) < 2,
        reason='Количество жанров меньше чем 2',
    )
    def test_set_book_genre_change_genre_genre_is_set(self):
        name = 'Название книги'
        self.collector.add_new_book(name)
        self.collector.set_book_genre(name, self.collector.genre[0])
        self.collector.set_book_genre(name, self.collector.genre[1])

        assert self.collector.books_genre[name] == self.collector.genre[1]

    def test_get_book_genre_empty_genre_empty_result(self):
        name = 'Название книги'
        self.collector.add_new_book(name)

        assert self.collector.get_book_genre(name) == ''

    @pytest.mark.parametrize('genre', BooksCollector().genre)
    def test_get_book_genre_genre_is_set_genre(self, genre):
        name = 'Название книги'
        self.collector.add_new_book(name)
        self.collector.set_book_genre(name, genre)

        assert self.collector.get_book_genre(name) == genre

    def test_get_book_genre_book_genre_not_set_None(self):
        assert self.collector.get_book_genre('Неизвестная книга') is None

    @pytest.mark.parametrize('genre', BooksCollector().genre)
    def test_get_books_with_specific_genre_genre_in_list_relevant_list(
        self,
        genre,
    ):
        books_count_for_genre = 5
        self.generate_book_list(books_count_for_genre)

        books_with_genre = self.collector.get_books_with_specific_genre(genre)
        for name in books_with_genre:
            assert self.collector.books_genre[name] == genre
        assert len(books_with_genre) == books_count_for_genre

    def test_get_books_with_specific_genre_wrong_genre_empty_list(self):
        self.generate_book_list()

        assert len(self.collector.get_books_with_specific_genre(
            'Неизвестный жанр',
        )) == 0

    def test_get_books_genre_genres_list(self):
        self.generate_book_list()

        assert self.collector.get_books_genre() == self.collector.books_genre

    def test_get_books_for_children_x_book_each_genre_relevant_list(self):
        books_count_for_genre = 5
        self.generate_book_list(books_count_for_genre)

        books_for_children = self.collector.get_books_for_children()
        for name in books_for_children:
            assert (
                self.collector.books_genre[name] not in
                self.collector.genre_age_rating
            )
        assert (
            len(books_for_children) ==
            books_count_for_genre * (
                len(self.collector.genre) -
                len(self.collector.genre_age_rating)
            )
        )

    def test_get_books_for_children_no_relevant_books_empty_list(self):
        self.generate_book_list(
            5,
            list(filter(
                lambda x: x not in self.collector.genre_age_rating,
                self.collector.genre,
            ))
        )

        assert len(self.collector.get_books_for_children()) == 0

    def test_add_book_in_favorites_add_two_books(self):
        books = ['Любимая книга 1', 'Любимая книга 2']
        for book in books:
            self.collector.add_new_book(book)
            self.collector.add_book_in_favorites(book)

        assert len(self.collector.favorites) == len(books)

    def test_add_book_in_favorites_already_added_not_added_twise(self):
        name = 'Любимая книга'
        self.collector.add_new_book(name)
        self.collector.add_book_in_favorites(name)
        self.collector.add_book_in_favorites(name)

        assert len(self.collector.favorites) == 1

    def test_add_book_in_favorites_book_not_in_list_empty_list(self):
        name = 'Любимая книга'
        self.collector.add_book_in_favorites(name)

        assert len(self.collector.favorites) == 0

    def test_delete_book_from_favorites_delete_two_books(self):
        books = ['Любимая книга 1', 'Любимая книга 2']
        for book in books:
            self.collector.add_new_book(book)
            self.collector.add_book_in_favorites(book)
        for book in books:
            self.collector.delete_book_from_favorites(book)

        assert len(self.collector.favorites) == 0

    def test_get_list_of_favorites_books_favorites_list(self):
        self.generate_book_list(1)
        for book in self.collector.books_genre:
            self.collector.add_book_in_favorites(book)

        assert (
            len(self.collector.get_list_of_favorites_books()) ==
            len(self.collector.books_genre)
        )
