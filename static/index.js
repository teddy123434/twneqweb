var about = document.getElementById("data");
var habit = document.getElementById("epicenter");
var timetable = document.getElementById("frequency");

about.addEventListener("click", function() {
	location.href = "/data";
});

habit.addEventListener("click", function() {
	location.href = "/epicenter";
});

timetable.addEventListener("click", function() {
	location.href = "/frequency";
});
