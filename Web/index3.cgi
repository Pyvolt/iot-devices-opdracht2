t <!DOCTYPE html>
t <html>
t <head>
t     <meta charset="UTF-8">
t     <title>LED Control</title>
t     <script language="JavaScript">
t         let pageFullyLoaded = false;
t         
t         function toggleLED() {
t             if(pageFullyLoaded) {
t                 document.form1.submit();
t             }
t         }
t         
t         function AllSW(st) {
t             for(i=0;i<document.form1.length;i++) {
t                 if(document.form1.elements[i].type=="checkbox"){
t                     document.form1.elements[i].checked=st;
t                 }
t             }
t             document.form1.submit();
t         }
t         
t         function pollButtonStatus() {
t             fetch("buttons.cgx").then(response => response.text())
t                 .then(data => {
t                     let parser = new DOMParser();
t                     let xmlDoc = parser.parseFromString(data, "text/xml");
t                     let checkboxes = xmlDoc.getElementsByTagName("checkbox");
t                     for(i=0; i<checkboxes.length && i<4; i++) {
t                         let on = checkboxes[i].getElementsByTagName("on")[0];
t                         if(on) {
t                             let rawValue = on.textContent;
t                             console.log("Button " + i + " raw value: '" + rawValue + "'");
t                             let status = rawValue === "true" ? "Released" : "Pressed";
t                             let element = document.getElementById("buttonStatus_" + i);
t                             if(element) {
t                                 element.textContent = status;
t                             }
t                         }
t                     }
t                 })
t                 .catch(error => {
t                     console.error("Error fetching button status:", error);
t                 });
t         }
t         
t         function pollPotentiometer() {
t             fetch("ad.cgx").then(response => response.text())
t                 .then(data => {
t                     let parser = new DOMParser();
t                     let xmlDoc = parser.parseFromString(data, "text/xml");
t                     let values = xmlDoc.getElementsByTagName("value");
t                     if(values.length > 0) {
t                         let hexValue = values[0].textContent;
t                         console.log(hexValue);
t                         let numVal = parseInt(hexValue, 16);
t                         console.log(numVal);
t                         let voltsVal = (13.2 * numVal) / 4096;
t                         console.log(voltsVal);
t                         let progressBar = document.getElementById("potentiometerBar");
t                         if(progressBar) {
t                             progressBar.value = voltsVal.toFixed(1);
t                         }
t                     }
t                 })
t                 .catch(error => {
t                     console.error("Error fetching potentiometer value:", error);
t                 });
t         }
t         
t         window.addEventListener("load", () => {
t             console.log("Page loaded, starting polling...");
t             pageFullyLoaded = true;
t             setInterval(pollButtonStatus, 2000);
t             setInterval(pollPotentiometer, 2000);
t         });
t     </script>
t </head>
t <body>
t     <h2 align="center">LED Control</h2>
t     <h3 align="center"><font size="2">Control LEDs 0-7 on the board using the checkboxes below.</font></h3>
t     <h3 align="center"><font size="2">View status of Buttons 1-4 on the board.</font></h3>
t     
t     <form action="index3.cgi" method="post" name="form1">
t         <input type="hidden" value="led" name="pg">
t         <table border="1" cellpadding="10" style="margin: 0 auto;">
t             <tr bgcolor="#aaccff">
t                 <th>LED Control [7..0]</th>
t             </tr>
t             <tr>
t                 <td align="center">
t                     <table>
t                         <tr valign="middle">
c b7                             <td><input type="checkbox" name="led7" onclick="toggleLED();" %s>7</td>
c b6                             <td><input type="checkbox" name="led6" onclick="toggleLED();" %s>6</td>
c b5                             <td><input type="checkbox" name="led5" onclick="toggleLED();" %s>5</td>
c b4                             <td><input type="checkbox" name="led4" onclick="toggleLED();" %s>4</td>
t                             <td width="5%"></td>
c b3                             <td><input type="checkbox" name="led3" onclick="toggleLED();" %s>3</td>
c b2                             <td><input type="checkbox" name="led2" onclick="toggleLED();" %s>2</td>
c b1                             <td><input type="checkbox" name="led1" onclick="toggleLED();" %s>1</td>
c b0                             <td><input type="checkbox" name="led0" onclick="toggleLED();" %s>0</td>
t                         </tr>
t                     </table>
t                 </td>
t             </tr>
t             <tr>
t                 <td align="center">
t                     <input type="button" value="  ON  " onclick="AllSW(true)">
t                     <input type="button" value="  OFF  " onclick="AllSW(false)">
t                 </td>
t             </tr>
t             <tr bgcolor="#e8f0f8">
t                 <th>Button Status [7..0]</th>
t             </tr>
t             <tr>
t                 <td align="center">
t                     <table>
t                         <tr valign="middle">
t                             <td>Button 3: <span id="buttonStatus_3">-</span></td>
t                             <td width="20px"></td>
t                             <td>Button 2: <span id="buttonStatus_2">-</span></td>
t                             <td width="20px"></td>
t                             <td>Button 1: <span id="buttonStatus_1">-</span></td>
t                             <td width="20px"></td>
t                             <td>Button 0: <span id="buttonStatus_0">-</span></td>
t                         </tr>
t                     </table>
t                 </td>
t             </tr>
t             <tr bgcolor="#e8f0f8">
t                 <th>Potentiometer Value</th>
t             </tr>
t             <tr>
t                 <td align="center">
t                     <label for="potentiometerBar">Potentiometer (0-13.2V):</label><br><br>
t                     <progress id="potentiometerBar" value="0" max="13.2"> 0% </progress>
t                 </td>
t             </tr>
t         </table>
t     </form>
t </body>
t </html>
.