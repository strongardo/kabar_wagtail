// Функция для получения и отображения количества просмотров
function fetchMaterialViews(material_id, views_element) {
    // Путь к Django view, который обрабатывает запрос
    const url = `/materials/get_views/${material_id}/`;

    // Отправляет AJAX запрос к серверу
    fetch(url)
        // Обрабатывает ответ от сервера. fetch возвращает промис, который решается объектом Response.
        // Метод .json() этого объекта читает ответ и преобразует его из формата JSON в JavaScript объект.
        .then(response => response.json())
        // В data будет находиться JavaScript объект, полученный в предыдущем then()
        .then(data => {
            // Обновляет содержимое на странице количеством просмотров
            views_element.textContent = data.views_count;
        })
        // Перехватывает ошибки, которые могли произойти на любом из предыдущих этапов
        .catch(error => console.error('Ошибка:', error));
}