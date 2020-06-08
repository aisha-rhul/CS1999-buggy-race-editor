window.onload = function () {
   $("#buggies tr").click(function(){
      $(this).addClass('selected').siblings().removeClass('selected');
      selected_id = $(this).find('td:first').html();
      sessionStorage.setItem("buggy_id", selected_id);

      document.getElementById("selected_id").value = $(this).find('td:first').html();
      document.getElementById("sel_primary_power").value = $(this).find('td:eq(2)').html();
      document.getElementById("sel_aux_power").value = $(this).find('td:eq(4)').html();
      document.getElementById("sel_flag_pattern").value = $(this).find('td:eq(8)').html();
      document.getElementById("sel_tyre_type").value = $(this).find('td:eq(10)').html();
      document.getElementById("sel_armour").value = $(this).find('td:eq(12)').html();
      document.getElementById("sel_attack").value = $(this).find('td:eq(13)').html();
      document.getElementById("sel_fireproof").value = $(this).find('td:eq(15)').html();
      document.getElementById("sel_insulated").value = $(this).find('td:eq(16)').html();
      document.getElementById("sel_antibiotic").value = $(this).find('td:eq(17)').html();
      document.getElementById("sel_banging").value = $(this).find('td:eq(18)').html();
      document.getElementById("sel_algo").value = $(this).find('td:eq(19)').html();
      document.getElementById("sel_cost").value = $(this).find('td:eq(20)').html();

   });
   drawFlag(pennant.pc,pennant.sc,pennant.pattern);
};