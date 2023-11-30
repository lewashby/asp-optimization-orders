enum products;
enum warehouses;

array[products, warehouses] of int: product_in_warehouse;
array[products] of int: product_request;
array[products] of int: product_price;
array[warehouses] of int: shipping_free_threshold;
array[warehouses] of int: shipping_fee;

int: allocate = max (p in products) (product_request[p]);

array[products, warehouses] of var 0..allocate: select;

constraint forall (p in products) (
  product_request[p] == sum (w in warehouses) (select[p, w])
);

constraint forall(w in warehouses, p in products) (
    select[p,w] <= product_in_warehouse[p,w]
);

function var int: final_cost(var int: total_price, int: free_threshold, int: cost) = 
  if total_price >= free_threshold then 0 else cost endif;

% minimize spedition cost
solve minimize sum (w in warehouses) (
  if sum (p in products) (select[p, w]) > 0 then 
      final_cost(
        sum (p in products) (select[p, w]*product_price[p]), 
        shipping_free_threshold[w], 
        shipping_fee[w]
      )
  else 0 endif
);



% minimize warehuse


% other
% solve minimize sum (w in warehouses) (sum (p in products) (shipping_fee[w]*select[p, w]));

% solve satisfy;
