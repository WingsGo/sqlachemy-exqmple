>>> from sqlalchemy import select
>>> product_higher_than_one_hundred = select([Product.id]).where(Product.price > 100.00)
>>>
>>> session = DBSession()
>>> session.query(Product).filter(Product.id.in_(product_higher_than_one_hundred)).all()
[( :u'CPU':300.0 ), ( :u'Motherboard':150.0 )]
>>> session.close()

>>> shopping_carts_with_products_higher_than_one_hundred = select([ShoppingCart.id]).where(
...     ShoppingCart.products.any(Product.id.in_(product_higher_than_one_hundred))
... )
>>> session = DBSession()
>>> session.query(ShoppingCart).filter(ShoppingCart.id.in_(shopping_carts_with_products_higher_than_one_hundred)).one()
( :John:[( :u'CPU':300.0 ), ( :u'Motherboard':150.0 )] )
>>> session.close()

>>> products_lower_than_one_hundred = select([Product.id]).where(Product.price < 100.00)
>>> from sqlalchemy import not_
>>> shopping_carts_with_no_products_lower_than_one_hundred = select([ShoppingCart.id]).where(
...     not_(ShoppingCart.products.any(Product.id.in_(products_lower_than_one_hundred)))
... )
>>> session = DBSession()
>>> session.query(ShoppingCart).filter(ShoppingCart.id.in_(
...     shopping_carts_with_no_products_lower_than_one_hundred)
... ).all()
[( :John:[( :u'CPU':300.0 ), ( :u'Motherboard':150.0 )] )]
>>> session.close()