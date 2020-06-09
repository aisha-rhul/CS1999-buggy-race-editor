  function autoFill() {
    document.getElementById("qty_wheels").value = "4";
    document.getElementById("power_type").value = "Petrol";
    document.getElementById("power_units").value = "1";
    document.getElementById("aux_power_type").value = "None";
    document.getElementById("aux_power_units").value = "0";
    document.getElementById("hamster_booster").value = "0";
    document.getElementById("flag_color").value = "#ffffff";
    document.getElementById("flag_pattern").value = "Plain";
    document.getElementById("flag_color_secondary").value = "#000000";
    document.getElementById("tyres").value = "Knobbly";
    document.getElementById("qty_tyres").value = "4";
    document.getElementById("armour").value = "None";
    document.getElementById("attack").value = "None";
    document.getElementById("qty_attacks").value = "0";
    document.getElementById("fireproof").checked = false;
    document.getElementById("insulated").checked = false;
    document.getElementById("antibiotic").checked = false;
    document.getElementById("banging").checked = false;
    document.getElementById("algo").value = "Steady";
  }

  function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

  function getRandomEven(min, max) {
    let even;
    do {
        even = getRandomInt(min, max)
    } while( even % 2 == 1 );
    return even
  }
 function getRandomColor() {
    let letters = '0123456789abcdef';
    let col= '#';
    for (let i = 0; i < 6; i++) {
        col += letters[Math.floor(Math.random() * 16)];
    }
    return col;
  }

  function randomFill() {
    document.getElementById("qty_wheels").value = getRandomEven(4,10).toString();
    document.getElementById("power_type").selectedIndex = getRandomInt(0,9);
    document.getElementById("power_units").value = getRandomInt(1,5).toString();
    document.getElementById("aux_power_type").selectedIndex = getRandomInt(0,10);
    document.getElementById("aux_power_units").value = getRandomInt(0,2).toString();
    document.getElementById("hamster_booster").value = getRandomInt(0,5).toString();;
    document.getElementById("flag_color").value = getRandomColor();
    document.getElementById("flag_pattern").selectedIndex = getRandomInt(0,5);
    document.getElementById("flag_color_secondary").value = getRandomColor();
    document.getElementById("tyres").selectedIndex = getRandomInt(0,4);
    document.getElementById("qty_tyres").value = getRandomInt(5,12).toString();
    document.getElementById("armour").selectedIndex = getRandomInt(0,5);
    document.getElementById("attack").selectedIndex = getRandomInt(0,4);
    document.getElementById("qty_attacks").value = getRandomInt(0,2).toString();
    document.getElementById("fireproof").checked = getRandomInt(0,1);
    document.getElementById("insulated").checked = getRandomInt(0,1);
    document.getElementById("antibiotic").checked = getRandomInt(0,1);
    document.getElementById("banging").checked = getRandomInt(0,1);
    document.getElementById("algo").selectedIndex = getRandomInt(0,5);
  }