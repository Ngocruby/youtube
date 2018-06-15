// Set margins
var margin = {
    top: 100,
    right: 10,
    bottom: 20,
    left: 30
  },
  width = 960 - margin.left - margin.right,
  height2 = 500 - margin.top - margin.bottom;
// x-Achse
var x = d3.scaleBand()
  .rangeRound([0, $('#bar').width()], .1);
//y-Achse
var y = d3.scaleLinear()
  .range([height2, 0]);

//Use our X scale to set a bottom axis
var xAxis = d3.axisBottom(x)
// Same for our left axis
var yAxis = d3.axisLeft(y)

var tip2 = d3.tip()
  .attr('class', 'd3-tip')
  .offset([-10, 0])
  .html(function (d) {
    return "<strong>Total:</strong> <span style='color:red'>" + d.total + "</span>";
  })
console.log(height2)

// Add our chart to the #bar div
var svg2 = d3.select("#bar").append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height2 + margin.top + margin.bottom)
  .append("g")
  .attr("id", "chart")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

svg2.call(tip2);
console.log("CHART");
var genresForLand;
d3.json("./json/youtube.json", function (error, youtube) {
  genresForLand = youtube.genresForLand;
  console.log(genresForLand); // nhan lai la 1 Object

 //lay het tat ca cac key(ten cac nuoc), Object.keys de chuyen Object thanh array
  var countryKeys = Object.keys(genresForLand);
  console.log(countryKeys);
  
  // Dropdown Countries
  var myDiv = document.getElementById("myDiv");

  //Create and append select list
  var selectList = document.createElement("select");
  selectList.setAttribute("id", "mySelect");
  myDiv.appendChild(selectList);

  //Create and add the Options to the DropDownList.
  for (var i = 0; i < countryKeys.length; i++) {
    var option = document.createElement("option");
    option.setAttribute("value", countryKeys[i]);
    option.text = countryKeys[i];
    selectList.appendChild(option);
  }

  var country = countryKeys[0]; // take the 1st value on coutryKey (in this case: Afghanistan)

  var data = genresForLand[country];
  console.log(data);

  drawMap(data);
});

/* function type(d) {
  d.total = +d.total;
  return d;
} */

$(document).on('change', '#mySelect', function (event) { // phat hien thay do cua ID: mySelect
  console.log(event);
  var value = event.target.value; // Lay ten nuoc
  console.log(value);
  var data = genresForLand[value];// genre cho nuoc do
  console.log(data);
  drawMap(data);
});


function drawMap(data) {  // define ve bieu do vao 1 funktion
  $("#chart").html('');

  x.domain(data.map(function (d) {
    return d.genre;
  }));

  y.domain([0, d3.max(data, function (d) {
    return d.total;
  })]);

  svg2.append("g")
    .attr("id", "bars")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height2 + ")")
    .call(xAxis);

  svg2.append("g")
    .attr("class", "y axis")
    .call(yAxis)
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 6)
    .attr("dy", ".71em")
    .style("text-anchor", "end")
    .text("Total");

  svg2.selectAll(".bar")
    .data(data)
    .enter().append("rect")
    .attr("class", "bar")
    .attr("x", function (d) {
      return x(d.genre);
    })
    .attr("width", x.bandwidth())
    .attr("y", function (d) {
      return y(d.total);
    })
    .attr("height", function (d) {
      return height2 - y(d.total);
    })
    .on('mouseover', tip2.show)
    .on('mouseout', tip2.hide);
}