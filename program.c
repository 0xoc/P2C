#include <stdio.h>
int main () {
float i;
i = 0;
l1:
if (i >= 10.0) goto l2;
printf("%f\n", i);
i += 1;
goto l1;
l2:;
return 0;
}