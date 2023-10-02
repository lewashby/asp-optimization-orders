% guess selection of products
{select(P,W,Q') : Q' = 0..@min(Q,R)} = 1 :-
  product_request(P,R),
  products_in_warehouse(P,W,Q).

% select the correct amount of products
:- product_request(P,R), #sum{Q,W : select(P,W,Q)} != R.

% minimize shipping cost
:~ warehouse_shipping_cost(W,C),
   warehouse_free_shipping(W,T),
   select(_,W,Q), Q > 0,
   #sum{Q' * Price,P : select(P,W,Q'), product_price(P,Price)} < T.
   [C@2, W]

% minimize warehouses
:~ warehouse(W), select(P,W,Q), Q > 0. [1@1, W]

#show.
#show select/3.