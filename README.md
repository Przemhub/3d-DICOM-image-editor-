
# Edytor obrazów 3d DICOM

Edytor markerów dla obrazów trójwymiarowych w odcieniach szarości odczytywanych z plików typu DICOM.

## Funkcjonalności:
-umożliwia zmianę stron obrazu przy pomocy kółka myszki, strzałek klawiatury oraz rysowanie swobodne linii markerów z użyciem myszki jako linii o dowolnym kształcie wewnątrz każdej strony.
-zwraca tablice współrzędnych (x,y,z) dla wszystkich linii markerów rysowanych przy pojedynczym wciśnięciu lewego przycisku myszki.
- rozróżnia co najmniej 2 typy markerów ( niebieski i czerwoni) odpowiadające zaznaczaniu podłoża i obiektu zainteresowania. 
- Kliknięcie prawym klawiszem myszki powinno usuwać w całości pojedynczą linię markera, którą pokazuje kursor myszy. 
- Zapisane dane markerów załadowywane są do edytora przy jego kolejnym użyciu i ponownie edytowane. 
 
 
## Zasoby:

Edytor został zrealizowany za pomocą języka Python:

- Interfejs graficzny – PyQT5

- Praca z plikami DICOM – pydicom

- Praca z obrazkami – matplotlib



Oprogramowanie, użyte do realizacji projektu:

- Visual Studio Code

- PyCharm

- PyQT5



## Wygląd i funkcjonalność:

![Zdjecie](https://media.discordapp.net/attachments/597512546504671234/826755092635975730/obszary.png)

1.	Wyświetlanie numeru warstwy zdjęcia na którym się znajdujemy
2.	Scroll bar ułatwiający przechodzenie po warstwach zdjęć
3.	Przyciski Object marker, base marker do wyboru typu markera
4.	Obszar do wyświetlania listy współrzędnych markerów



Zakładka ‘File’ zawiera 4 przyciski:

- Open – otwieranie plików

- Load Project – otwieranie wcześniej zapisanych markerów z pliku json

- Save – zapisanie wprowadzonych markerów do pliku json

- Exit – zamykanie programu

![Markery](https://media.discordapp.net/attachments/597512546504671234/826757165380403230/kreski.png?width=605&height=455)



## Elementy interfejsu:

- Slider po lewo – zmiana warstwy (również może być wykorzystane kółko myszki)

- Obrazek po środku – podgląd obecnie wybranej warstwy, rysowanie i pokazywanie markerów

- Przyciski ‘Object marker’ i ‘Base marker’ – wybór rodzaju markera (Object marker – czerwony kolor, Base marker – niebieski kolor)

- Lista punktów – lista zawierająca informację o punktach składowych markerów (współrzędne x i y, warstwa).

- Slider ‘Precision’ – pozwala na zwiększenie lub zmniejszenie precyzji rysowania markerów

- Status – zawiera informację o obecnie wybranej warstwie i pozycji kursora myszki

## Instrukcja:

Otwieramy plik za pomocą przycisku File -> Open lub przeciągając plik z eksploratora do programu (openFileNameDialog() lub dragEnterEvent() + dropEvent()).

Warstwy zmieniamy za pomocą slidera lub kółka myszki (valueChange() lub mouseMoveEvent()).

Markery są rysowane za pomocą myszki. Po wciśnięciu jednego z przycisków wyboru rodzaju markera (objectMarker() lub baseMarker()) możemy, utrzymując lewy przycisk myszy (mousePressEvent()), wskazać jego kształt (paintEvent() + mouseMoveEvent() + get_line(start, end) + mouse(x, y, z) ). W zależności od pozycji slidera ‘Precision’ możemy zmieniać precyzję rysowania markera (valueChangePrecision()).

Jeżeli któryś z markerów nie jest nam już potrzebny, to możemy łatwo go usunąć za pomocą prawego przyciska myszki (mousePressEvent() + mouseMoveEvent()).

Po dodaniu wszystkich markerów możemy zapisać zmiany do pliku json za pomocą przycisku File -> Save (saveFileDialog()), i później go otworzyć za pomocą przycisku File -> Load Project (loadFileDialog()).



## Klasy i funkcję:

Klasa MainWindow – zawiera funkcje obsługujące okna dialogowe:

- closeEvent() – zamykanie aplikacji

- openFileNameDialog() – otwieranie plików

- loadFileDialog() – otwieranie pliku json

- saveFileDialog() – zapisywanie zmian do pliku json



Klasa MainWidget – zawiera funkcje obsługujące wybór markerów

- changeImage(filename) – wywołanie funkcji changeImage() z klasy ImageWidget

- objectMarker() – ustawianie typu markera objectMarker

- baseMakrer() - ustawianie typu markera baseMarker



Klasa ImageWidget - zawiera funkcje obsługujące rysowanie markerów

- valueChange() – odczyt danych ze slidera i zmiana warstwy

- valueChangePrecision() - odczyt danych ze slidera i zmiana precyzji rysowania

- updateImage() – odświeżanie obrazku i statusu

- paintEvent() – pozwala rysować na obrazku

- wheelEvent() – obsługa kółka myszki dla zmiany warstwy

- mouseMoveEvent() – obsługa przemieszczenia kursora myszki, rysowania i usuwania markerów

- resizeEvent() – obsługa zmiany rozmiary okna programu

- dragEnterEvent() – decyduje czy najeżdżamy na aplikację myszką z plikiem, czy bez pliku

- dropEvent() – obsługa otwierania pliku przez przeciągnięcie pliku z eksploratora plików do programu

- mousePressEvent() – obsługa wciskania przycisków myszki oraz ustawianie startowych współrzędnych dla rysowania

- mouseReleaseEvent() – obsługa … przycisków myszki oraz dopisywanie markerów do listy

- changeImage(filename) – zmiana obrazku oraz niezbędne zmiany wartości zmiennych przy zmianie obrazku

- get_line(start, end) – połączenie punktów za pomocą algorytmu Bresenhama

- mouse(x, y, z) – dodanie punktów markerów do listy

- drawOnImage() – rysowanie markera

- clearOutput() – czyszczenie listy punktów markerów



## Testy

Dokładność rysowania markerów przy różnych wartościach Precision:

### MAX:


![Max](https://media.discordapp.net/attachments/597512546504671234/826757167507439666/max.png)

### MID:

![Mid](https://media.discordapp.net/attachments/597512546504671234/826757169390026762/mid.png)


### MIN:


![Min](https://media.discordapp.net/attachments/597512546504671234/826757161178759181/min.png)

## Podsumowanie

Dla realizowania zadania użyto języka Python oraz różnych bibliotek: PyQT5 do interfejsu użytkownika, pydicom do pracy z plikami DICOM itd. Udało nam się w termonach zrealizować wszystko, co zaplanowaliśmy w harmonogramie, wynik końcowy spełnia wszystkie zagadnienia, które otrzymaliśmy w zadaniu.

Możliwy rozwój w przyszłości

Jako kolejne korki rozwoju tego projektu można zaproponować:

- rozszerzenie ustawień markerów do zmiany koloru i grubości markerów

- obsługa innych formatów plików

- obsługa innych sposobów zapisywania i przechowywania informacji

- optymizacja interfejsu użytkownika


Bibliografia: http://www.roguebasin.com/index.phptitle=Bresenham%27s_Line_Algorithm#Python - zastosowanie algorytmu Bresenhama w różnych językach http://0x80.pl/articles/bresenham.html - artykuł na temat teorii algorytmu Bresenhama
