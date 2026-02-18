let pageFullyLoaded = false;
let potentiometerHistory = [];

google.charts.load('current', {'packages':['corechart']});

function toggleLED() {
    if(pageFullyLoaded) {
        document.form1.submit();
    }
}

function AllSW(st) {
    for(i=0;i<document.form1.length;i++) {
        if(document.form1.elements[i].type=="checkbox"){
            document.form1.elements[i].checked=st;
        }
    }
    document.form1.submit();
}

function pollButtonStatus() {
    fetch("buttons.cgx").then(response => response.text())
        .then(data => {
            let parser = new DOMParser();
            let xmlDoc = parser.parseFromString(data, "text/xml");
            let checkboxes = xmlDoc.getElementsByTagName("checkbox");
            for(i=0; i<checkboxes.length && i<4; i++) {
                let on = checkboxes[i].getElementsByTagName("on")[0];
                if(on) {
                    let rawValue = on.textContent;
                    console.log("Button " + i + " raw value: '" + rawValue + "'");
                    let status = rawValue === "true" ? "Released" : "Pressed";
                    let element = document.getElementById("buttonStatus_" + i);
                    if(element) {
                        element.textContent = status;
                    }
                }
            }
        })
        .catch(error => {
            console.error("Error fetching button status:", error);
        });
}

function pollPotentiometer() {
    fetch("ad.cgx").then(response => response.text())
        .then(data => {
            let parser = new DOMParser();
            let xmlDoc = parser.parseFromString(data, "text/xml");
            let values = xmlDoc.getElementsByTagName("value");
            if(values.length > 0) {
                let hexValue = values[0].textContent;
                let numVal = parseInt(hexValue, 16);
                let voltsVal = (13.2 * numVal) / 4096;
                console.log("Potentiometer VoltValue: " + voltsVal);
                let progressBar = document.getElementById("potentiometerBar");
                if(progressBar) {
                    progressBar.value = voltsVal.toFixed(1);
                }
                potentiometerHistory.push(voltsVal.toFixed(2));
                if(potentiometerHistory.length > 60) {
                    potentiometerHistory.shift();
                }
                drawPotentiometerChart();
            }
        })
        .catch(error => {
            console.error("Error fetching potentiometer value:", error);
        });
}

function drawPotentiometerChart() {
    if(potentiometerHistory.length === 0) return;
    
    let chartData = [['Sample', 'Voltage (V)']];
    for(let i = 0; i < potentiometerHistory.length; i++) {
        chartData.push(['' + (i + 1), parseFloat(potentiometerHistory[i])]);
    }
    
    let data = google.visualization.arrayToDataTable(chartData);
    
    let options = {
        title: 'Potentiometer Voltage History (Last 60 samples)',
        curveType: 'function',
        legend: { position: 'bottom' },
        hAxis: {
            title: 'Sample Number'
        },
        vAxis: {
            title: 'Voltage (V)',
            minValue: 0,
            maxValue: 13.2
        }
    };
    
    let chart = new google.visualization.LineChart(document.getElementById('potentiometer_chart'));
    chart.draw(data, options);
}

window.addEventListener("load", () => {
    console.log("Page loaded, starting polling...");
    pageFullyLoaded = true;
    setInterval(pollButtonStatus, 2000);
    setInterval(pollPotentiometer, 5000);
});
