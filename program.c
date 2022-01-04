
        #include <stdio.h>
        
        int main () {
            float t1 = 3.0 + 3.0;
float a = t1;
float b = 6.0;
float t2 = -2.0;
float result = t2;
float t3 = a > b;

float t4 = a == b;

if (!t3) goto l2;
result = 1.0;

goto l1;
l2:;
if (!t4) goto l3;
result = 0.0;

goto l1;
l3:;
float t5 = -1.0;
result = t5;

l1:;
printf("%f\n", result);

            return 0;
        }
        