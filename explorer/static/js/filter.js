function Counter(array) {
  var count = {};
  array.forEach(val => count[val] = (count[val] || 0) + 1);
  return count;
}

function isHidden(el) {
    var style = window.getComputedStyle(el);
    return (style.display === 'none')
}

function updateCounters(){
    let table = document.getElementById("table");
    let texts = [];
    for (let row of table.rows) {
        let text = '';
        for(let cell of row.cells)
        {
            if (!isHidden(cell) && cell.id != 'counter'){
                text += cell.innerHTML;
            }

        }
        texts.push(text);
    }
    let counter = Counter(texts);
    for (let row of table.rows) {
        let text = '';
        for(let cell of row.cells)
        {
            if (!isHidden(cell) && cell.id != 'counter'){
                text += cell.innerHTML;
            }
            else if(cell.id == 'counter'){
                cell.innerHTML = counter[text];
                console.log(cell.innerHTML)
            }
        }
    }
}

$(function(){
    $(".toggler").click(function () {
        $(this).toggleClass('btn-primary');
        let columnClass = '.' + $(this).val();
        $(columnClass).toggle();
        updateCounters();
    });
});


