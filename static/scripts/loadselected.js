 window.onload = function () {
    document.getElementById("power_type").value=capitalise(opt.sel_primary_power);
    document.getElementById("aux_power_type").value=capitalise(opt.sel_aux_power);
    document.getElementById("flag_pattern").value=capitalise(opt.sel_flag_pattern);
    document.getElementById("tyres").value=capitalise(opt.sel_tyre_type);
    document.getElementById("armour").value=capitalise(opt.sel_armour);
    document.getElementById("attack").value=capitalise(opt.sel_attack);

    document.getElementById("fireproof").checked=JSON.parse(opt.sel_fireproof);
    document.getElementById("insulated").checked=JSON.parse(opt.sel_insulated);
    document.getElementById("antibiotic").checked=JSON.parse(opt.sel_antibiotic);
    document.getElementById("banging").checked=JSON.parse(opt.sel_banging);

    document.getElementById("algo").value=capitalise(opt.sel_algo);
 }

 const capitalise = (str, lower = false) =>
  (lower ? str.toLowerCase() : str).replace(/(?:^|\s|["'([{])+\S/g, match => match.toUpperCase());
