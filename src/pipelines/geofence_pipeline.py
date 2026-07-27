import math
import streamlit as st
import streamlit.components.v1 as components
from src.config.geofence_config import (
    COLLEGE_LAT,
    COLLEGE_LNG,
    ALLOWED_RADIUS_METERS,
    GEOFENCE_ENABLED
)


def get_distance_meters(lat1, lng1, lat2, lng2):
    R      = 6371000
    phi1   = math.radians(lat1)
    phi2   = math.radians(lat2)
    dphi   = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)

    a = (
        math.sin(dphi / 2) ** 2 +
        math.cos(phi1) * math.cos(phi2) *
        math.sin(dlambda / 2) ** 2
    )

    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def is_inside_campus(student_lat, student_lng):
    distance = get_distance_meters(
        student_lat, student_lng,
        COLLEGE_LAT, COLLEGE_LNG
    )
    return distance <= ALLOWED_RADIUS_METERS, round(distance)


def get_gps_html():
    return """
    <div id="gps-status" style="
        background: #E0E3FF;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        font-family: Arial, sans-serif;
        margin-bottom: 10px;
    ">
        <p id="status-text" style="margin:0; color:#5865F2; font-weight:bold;">
            📍 Getting your location...
        </p>
    </div>

    <input type="hidden" id="lat-input">
    <input type="hidden" id="lng-input">
    <input type="hidden" id="acc-input">

    <button onclick="getLocation()" style="
        background: #5865F2;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 24px;
        font-size: 1rem;
        cursor: pointer;
        width: 100%;
        margin-bottom: 8px;
    ">
        📍 Get My Location
    </button>

    <button onclick="sendLocation()" id="send-btn" style="
        background: #2ECC71;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 24px;
        font-size: 1rem;
        cursor: pointer;
        width: 100%;
        display: none;
    ">
        ✅ Confirm Location
    </button>

    <script>
    var userLat = null;
    var userLng = null;
    var userAcc = null;

    function getLocation() {
        var statusEl = document.getElementById('status-text');
        statusEl.innerHTML = '🔄 Detecting location...';

        if (!navigator.geolocation) {
            statusEl.innerHTML = '❌ GPS not supported by your browser';
            return;
        }

        navigator.geolocation.getCurrentPosition(
            function(pos) {
                userLat = pos.coords.latitude;
                userLng = pos.coords.longitude;
                userAcc = pos.coords.accuracy;

                document.getElementById('lat-input').value = userLat;
                document.getElementById('lng-input').value = userLng;
                document.getElementById('acc-input').value = userAcc;

                statusEl.innerHTML = (
                    '✅ Location found!<br>' +
                    '📍 Lat: ' + userLat.toFixed(6) + '<br>' +
                    '📍 Lng: ' + userLng.toFixed(6) + '<br>' +
                    '🎯 Accuracy: ±' + Math.round(userAcc) + ' meters'
                );

                document.getElementById('send-btn').style.display = 'block';
            },
            function(err) {
                var msg = '';
                if (err.code === 1) msg = '❌ Location permission denied. Please allow location access.';
                else if (err.code === 2) msg = '❌ Location unavailable. Please try again.';
                else if (err.code === 3) msg = '❌ Location timeout. Please try again.';
                else msg = '❌ Unknown error: ' + err.message;
                statusEl.innerHTML = msg;
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            }
        );
    }

    function sendLocation() {
        if (userLat && userLng) {
            window.parent.postMessage({
                type: 'LOCATION',
                lat:  userLat,
                lng:  userLng,
                acc:  userAcc
            }, '*');

            document.getElementById('status-text').innerHTML =
                '📤 Location sent! Please wait...';
        }
    }

    getLocation();
    </script>
    """


def geofence_check_ui():
    if not GEOFENCE_ENABLED:
        return True

    if st.session_state.get('geofence_passed'):
        return True

    st.markdown("""
    <div style="
        background: #E0E3FF;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
    ">
        <h3 style="color: #5865F2; margin: 0;">📍 Location Verification</h3>
        <p style="color: #333; margin: 8px 0 0 0;">
            You must be inside campus to mark attendance
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("🎯 Required",  f"Inside Campus")
    col2.metric("📏 Radius",    f"{ALLOWED_RADIUS_METERS}m")
    col3.metric("🏫 Campus",    "College Location")

    st.write("")

    components.html(get_gps_html(), height=280)

    st.write("")
    st.write("**Enter your coordinates manually** (if GPS fails):")

    c1, c2 = st.columns(2)
    with c1:
        manual_lat = st.text_input("Latitude",  placeholder="e.g. 26.4499", key="manual_lat")
    with c2:
        manual_lng = st.text_input("Longitude", placeholder="e.g. 80.3319", key="manual_lng")

    if st.button("📍 Check My Location", type="primary", width="stretch", key="check_location_btn"):
        lat = None
        lng = None

        if manual_lat and manual_lng:
            try:
                lat = float(manual_lat)
                lng = float(manual_lng)
            except ValueError:
                st.error("❌ Invalid coordinates. Please enter valid numbers.")
                return False

        if lat is None or lng is None:
            st.warning("⚠️ Please enter your coordinates or use the GPS button above.")
            return False

        inside, distance = is_inside_campus(lat, lng)

        if inside:
            st.success(f"✅ You are inside campus! (Distance: {distance}m from center)")
            st.session_state.geofence_passed = True
            st.session_state.student_location = {"lat": lat, "lng": lng}
            import time
            time.sleep(1)
            st.rerun()
        else:
            st.error(
                f"❌ You are outside campus!\n\n"
                f"📏 Your distance: {distance}m\n"
                f"🎯 Allowed radius: {ALLOWED_RADIUS_METERS}m\n\n"
                f"Please come to college campus to mark attendance."
            )

    if st.button("🔓 Skip Location Check (Demo Mode)", type="secondary", width="stretch", key="skip_geo"):
        st.session_state.geofence_passed = True
        st.warning("⚠️ Skipped location check — Demo mode only!")
        import time
        time.sleep(1)
        st.rerun()

    return False