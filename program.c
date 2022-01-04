#include <stdio.h>
int main () {
float a = 10.0;
l1: 
if (!a) goto l2;
a -= 1.0;
printf("%f\n", a);
goto l1;
l2:;
printf("%f\n", a);
return 0;
}