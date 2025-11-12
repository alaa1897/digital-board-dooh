from django.shortcuts import render
from user.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required(login_url='login')
def dashboard_client(request):
    
    client = request.user 
    if client.role !='client':
        return redirect('login')

    else:
        first_name = client.first_name
        total_ads = client.ads_belonging_for_this_client()
        number_total_ads = client.ads_count()
        active_ads_number = client.active_ads_for_this_client().count()
        pending_ads_number = client.pending_ads_for_this_client().count()
        approved_ads_number = client.approved_ads_for_this_client().count()
        rejected_ads_number = client.rejected_ads_for_this_client().count()
        recent_ads = client.ads_belonging_for_this_client().order_by('-uploaded_at')[:3]
        recent_ads = total_ads.order_by('-uploaded_at')[:3]
        
        prepared_ads = []
        for ad in recent_ads:
             board_locations = ", ".join(board.location for board in ad.boards.all()) or "Not Assigned"
             prepared_ads.append({
            'title': ad.title,
            'media_type': ad.media_type,
            'statue': ad.statue.capitalize(),
            'badge_class': (
            'badge-success' if ad.statue == 'active' else
            'badge-warning' if ad.statue == 'pending' else
            'badge-danger' if ad.statue == 'rejected' else
            'badge-secondary'
            ),
            'board_locations': board_locations,
            'uploaded_at': ad.uploaded_at,
        })

    context = {
        'first_name': first_name,
        'number_of_total_ads': number_total_ads,
        'active_ads_number': active_ads_number,
        'pending_ads_number': pending_ads_number,
        'approved_ads_number': approved_ads_number,
        'rejected_ads_number': rejected_ads_number,
        'prepared_ads': prepared_ads,
    }
    return render(request, "client/client_dashboard.html", context)



"""
 {% if number_of_total_ads == 0 %}
    <div class="card">
        <div class="empty-state-icon">📭</div>
            <h3>No ads to display yet</h3>
"""