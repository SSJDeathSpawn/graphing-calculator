
sign = lambda x: x and [1, -1][x<0]
lerp = lambda a,b,t: (1 - t) * a + t * b;
invlerp = lambda a,b,v: [(v-a)/(b-a), a][b==a]