var width = window.outerWidth, // xac dinh chieu dai cua Browser -Detect Browser-Width
    height = window.outerHeight; //xac dinh chieu cao

var svg = d3.select("body") // chon body element
    .append("svg") // them svg vao body - append la funktion
    .attr("width", width) // set do dai cho svg - attr la atrribut
    .attr("height", height)// set chieu cao cho svg
    .append('g') // them element g vao trong svg - g viet tat cua group
    .attr('class', 'map'); // them attribu class ten map - add attribut

var projection = d3.geoMercator() // tao projection Mercator
    .scale(200) // xet do zoom- so cang nho zoom cang nhieu
    .translate([width / 2, height / 1.5]); // xac dinh toa do

var path = d3.geoPath().projection(projection); // xac dinh duong ve theo projection

queue() // bat dau xep hang
    .defer(d3.json, "json/world_countries.json") // dan file json
    .defer(d3.json, "json/youtube.json")
    .await(ready); // goi funktion ve ban do

function ready(error, world_countries, youtube) {
    console.log(world_countries); // log la in ra trong console
    console.log(youtube);
    var videos = youtube.videos; // videos va overlay la objekt trong file youtube goi ra de su dung
    var overlay = youtube.overlay;

    svg.append("g")
        .attr("class", "countries") 
        .selectAll("path") // chon tat ca path trong group countries
        .data(world_countries.features) //features la objekt trong world_countries
        .enter().append("path") // hanh dong ve
        .attr("d", path) // them atrribut net ve la d
        .style("fill", function(country) {
            var id = country.id; // Get Country ID in World Map
            var filterVideos = videos.filter(function(video) {
                return video.alpha3Code === id; // check if country ID in Videos is the same as country ID in World Mao
            }); // return la truth or falsch tuong duong vs if
            console.log(filterVideos);
            if (filterVideos[0]) { // Check if video exists
                var videoId = filterVideos[0].video.id; // Get Video ID
                var color = overlay[videoId].color; // Get Color
                return color;
            }
            return '#aaaaaa';
        })
        .style('stroke', 'white') // cho vien mau trang
        .style('stroke-width', 1.5) // do dam nhat cua vien
        .style("opacity", 0.8) // do transparent
        .on('mouseover', function(d) { // neu de chuot vao
            d3.select(this) // this dc tu hieu la path vi selectALL o tren
                .style("opacity", 1)
                .style("stroke-width", 3);
        })
        .on('mouseout', function(d) { // neu di chuot ra
            d3.select(this)
                .style("opacity", 0.8)
                .style("stroke-width", 1.5);
        });    
}