#include <stdio.h>
int main () {
float a = 10.0;
float b = 30.0;
float t1 = a * b;
float t2 = 2.0 * a;
float t3 = 4.0 * b;
float t4 = t2 + t3;
float t5 = t1 / t4;
float c = t5;
float t6 = c < 2.0;
float t7 = c > 2.0;
if (!t6) goto l6;
printf("C is less than 2");
goto l5;
l6:;
if (!t7) goto l7;
float m = 10.0;
float t8 = m > 0.0;
l3: 
if (!t8) goto l4;
float t9 = 10.0 - m;
printf("Iteration %f\n", t9);
float i;
i = 0;
l1:
if (i >= m) goto l2;
printf("\tI: %f\n", i);
i += 1;
goto l1;
l2:;
m -= 1.0;
t8 = m > 0.0;
goto l3;
l4:;
goto l5;
l7:;
printf("C is exactly 2");
l5:;
printf("C:g %f\n", c);
return 0;
}