/*function dispGraph(){*/
  var names = [];
  var numbers = [];
  var items = document.getElementsByClassName("item");
  var values = document.getElementsByClassName("value");
  for (var i = 0; i < items.length; i++) {
    console.log(items[i]);
    names.push(items[i].value);
  }

  for (var i = 0; i < values.length; i++) {
    const idx = i;
    console.log(numbers[i]);
    numbers.push(values[i].value);
/*    values[i].addEventListener("change", function(e) {
      numbers[idx] = e.target.value;
      console.log(idx);
      chart.update();
      console.log(values[i].value)
    });*/
  }
/*  console.log(items);
  console.log(numbers);*/
  var ctx = document.getElementById("mycanvas");
  var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Jan','Feb','Mar','Apr','May'],
/*      labels: names,*/
      datasets: [{
        label: 'Blue',
        data: [30, 20, 15],
/*        data: numbers,*/
        backgroundColor: '#48f',
      }],
    }
  });
/*  chart.render();*/


/*function disp(){
  var names = []
  var numbers = [];
  var items = document.getElementsByClassName("item");
  var values = document.getElementsByClassName("value");
  for (var i = 0; i < items.length; i++) {
    console.log(items[i]);
    names.push(items[i].value);
  }

  for (var i = 0; i < values.length; i++) {
    const idx = i;
    console.log(numbers[i]);
    numbers.push(values[i].value);*/
/*    values[i].addEventListener("change", function(e) {
      numbers[idx] = e.target.value;
      console.log(idx);
      chart.update();
      console.log(values[i].value)
    });*/
/*  }*/
/*  console.log(items);
  console.log(numbers);
  var ctx = document.getElementById("mycanvas");
  var myChart = new Chart(ctx, {
    type: 'bar',
    data: {*/
/*      labels: ['Jan','Feb','Mar','Apr','May'],*/
/*      labels: names,
      datasets: [{
        label: 'Blue',
        data: [30, 20, 15],
        data: numbers,
        backgroundColor: '#48f',
      }],
    },
  });
}*/


/*
  var x = {{ result|tojson }};
  target = document.getElementById("output");
  target.innerHTML = x;
*/