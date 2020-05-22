function huoqu() {
	var a = document.getElementById("date1").value;
	var b = document.getElementById("date2").value;
	var date1 = new Date(a);
	var date2 = new Date(b);
	var date3 = date2.getTime() - date1.getTime();
	var days = Math.floor(date3 / (24 * 3600 * 1000) + 1);
	document.getElementById("days").value = days;
};