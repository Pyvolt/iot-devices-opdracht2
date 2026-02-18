t <!DOCTYPE html>
t <html>
t <head>
t     <meta charset="UTF-8">
t     <title>LED Control</title>
t     <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
t    <script type="text/javascript" src="script.js"></script>
t </head>
t <body>
t     <h2 align="center">LED Control</h2>
t     <h3 align="center"><font size="2">Control LEDs 0-7 on the board using the checkboxes below.</font></h3>
t     <h3 align="center"><font size="2">View status of Buttons 1-4 on the board.</font></h3>
t     <h3 align="center"><font size="2">View level of the onboard potentiometer.</font></h3>
t     
t     <form action="index2.cgi" method="post" name="form1">
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
t             <tr bgcolor="#e8f0f8">
t                 <th>Potentiometer History</th>
t             </tr>
t             <tr>
t                 <td align="center">
t                     <div id="potentiometer_chart" style="width: 900px; height: 500px"></div>
t                 </td>
t             </tr>
t         </table>
t     </form>
t </body>
t </html>
.