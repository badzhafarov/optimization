// piavskii method / метод Пиявского / метод ломаных

#include <stdio.h>
#include <iostream>
#include <math.h>
#include <vector>
#include <algorithm>
#include <functional>
#include <iterator>

using namespace std;

int i, k(3);
double leftBorder(-10), rightBorder(8), lipschitz(4), eps(0.01), minValue, uLeft, uRight, minIndex, uPrevious, uNext;

double f(double x){
    return 5+3*sin(x)+x;
}

double g(double x2, double x1){
    return f(x2)-lipschitz*fabs(x1-x2);
}

double u(double x1, double x2){
    return (f(x1)-f(x2))/(2*lipschitz) +(x1+x2)/2;
}

class double_vector{
public:
    double_vector(double p, double v);
    bool operator <(const double_vector&) const;
    double point, value;
};

bool double_vector::operator<(const double_vector& self) const{
    return point < self.point;
}

double_vector::double_vector(double p, double v): point(p), value(v) {}

int main(){
    vector<double_vector> v;
    v.push_back(double_vector(leftBorder, f(leftBorder))); // first point
    v.push_back(double_vector(rightBorder, f(rightBorder))); // second point
    uPrevious = rightBorder;
    uNext = u(leftBorder, rightBorder);
    v.push_back(double_vector(uNext, g(uNext, leftBorder))); // third point
    minIndex = 1; // at the beginning minimal value have third point, it is located between the left (0) border and right (2) borders
    sort(v.begin(), v.end(), less<double_vector>());
    while (fabs(f(uNext) - g(uPrevious, uNext)) >= eps){
        ++k;
        minValue = uNext;
        v[minIndex].value=f(v[minIndex].point);
        
        uLeft = u(v[minIndex - 1].point, v[minIndex].point);
        v.push_back(double_vector(uLeft, g(uNext, uLeft)));
        
        uRight = u(v[minIndex].point, v[minIndex + 1].point);
        v.push_back(double_vector(uRight, g(uNext, uRight)));
        
        sort(v.begin(), v.end(), less<double_vector>());
        minValue = (*min_element(v.begin(),v.end())).value;
        minIndex = distance(v.begin(), min_element(v.begin(),v.end()));
        
        for (int i = 0; i < static_cast<int> (v.size()); ++i){
            if (v[i].value < minValue){
                minValue = v[i].value;
                minIndex = i;
            }
        }
        uPrevious = uNext;
        uNext = v[minIndex].point;
        cout << "x* = " << uNext << " f(x*) = " << f(uNext) << " Iter: " << k << endl;
    }
    return 0;
}
