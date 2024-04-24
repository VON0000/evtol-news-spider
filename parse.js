async () => {
    const pTags = document.querySelectorAll('p');

    let targetUl;

    pTags.forEach(p => {
        if (p.querySelector("strong") && p.querySelector("strong").textContent === "Specifications:") {
            targetUl = p.nextElementSibling;
        }
    });

    const result = {}

    let lst = [];

    const listItems = targetUl.querySelectorAll('li');

    listItems.forEach(li => {
        lst = [...lst, li.textContent];
    })

    result['title'] = document.querySelector('h1').textContent;
    result['url'] = window.location.href;
    result['Specifications'] = lst;

    return result;
}