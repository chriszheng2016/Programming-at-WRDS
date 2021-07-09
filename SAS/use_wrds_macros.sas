%include "/wrds/wrdsmacros/winsorize.sas";

data month_return_raw;
  set crsp.msf (obs=100);
  keep date cusip permo ret;
run;

proc print data = month_return_raw;
run;

%WINSORIZE(INSET=month_return_raw,OUTSET=month_return,SORTVAR=date,VARS=ret);
run;

proc print data = month_return;
run;