async () => {
    let lst = [];

    const parentNode = document.querySelectorAll("[class=\"col-sm-6\"]");

    // 对每个符合条件的元素，选择其下的所有 'li' 标签
    parentNode.forEach(element => {
        const listItems = element.querySelectorAll('li a');
        listItems.forEach(li => {
            lst = [...lst, li.href];
        });
    });
    console.log(lst)
    return lst
}