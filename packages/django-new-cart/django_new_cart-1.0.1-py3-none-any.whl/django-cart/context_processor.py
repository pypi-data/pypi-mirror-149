def cart_total_amount(request):
	if request.user.is_authenticated:
		return {'cart_total_amount' : 
			sum(map( # Map all prices multiplied by quantities for later sum
				lambda x: (
					float(x["product"].price) * x["product"].quantity
				),
				dict(request.session['cart']).values()))
		} 
	else:
		return {'cart_total_amount' : 0} 