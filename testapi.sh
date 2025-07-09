#!/bin/bash

set -e

EMAIL="${1:-fatima.azeemuddin@outlook.com}"
PASSWORD="${2:-Password@123}"
FULL_NAME="${3:-Fatima Azeemuddin}"
IS_TERM_ACCEPTED="${4:-true}"

DB_URL="postgres://postgres:123456789@localhost:5482/authentication_app"

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

section() {
  echo -e "\n${CYAN}========== $1 ==========${NC}\n"
}

success() {
  echo -e "${GREEN}✔ $1${NC}"
}

fail() {
  echo -e "${RED}✖ $1${NC}"
  exit 1
}

# SECTION 1: Clean up
section "Database Cleanup"
psql "$DB_URL" -c 'DELETE FROM "user";' > /dev/null && success "All user records deleted"

# SECTION 2: Registration
section "User Registration"
REGISTER_RESPONSE=$(curl -s -X POST http://127.0.0.1:8000/api/v1/register \
  -H "x-api-key: PYHXCbfqwdER19IcyHJxpImJgIchKxlziNyvP59lWVk=" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\",\"full_name\":\"$FULL_NAME\",\"is_term_accepted\":$IS_TERM_ACCEPTED}")

echo "$REGISTER_RESPONSE" | grep -q "Registration successful" && success "Registration API returned success" || fail "Registration failed"

# SECTION 3: User Table Check
section "User Table"
psql "$DB_URL" -c 'SELECT id, email FROM "user";'

# SECTION 4: OTP Table Check & Fetch
section "OTP Table"
OTP_CODE=$(psql "$DB_URL" -t -A -c 'SELECT code FROM "otp" ORDER BY created_at DESC LIMIT 1;')
if [[ -z "$OTP_CODE" ]]; then
  fail "No OTP records found!"
else
  success "OTP code fetched: $OTP_CODE"
fi
psql "$DB_URL" --pset pager=off -c 'SELECT  user_id, code, type, expires_at FROM "otp" ORDER BY created_at DESC LIMIT 1;'

# SECTION 5: OnBoarding Table Check
section "OnBoarding Table"
psql "$DB_URL" -c 'SELECT user_id, full_name, completed FROM "on_boarding" ORDER BY created_at DESC LIMIT 1;'

# SECTION 6: OTP Verification
section "OTP Verification"
VERIFY_RESPONSE=$(curl -s -X POST http://127.0.0.1:8000/api/v1/verify-otp \
  -H "x-api-key: PYHXCbfqwdER19IcyHJxpImJgIchKxlziNyvP59lWVk=" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"otp\":\"$OTP_CODE\"}")

echo "$VERIFY_RESPONSE" | grep -q "Email verified successfully" && success "OTP verification API returned success" || fail "OTP verification failed"

# SECTION 7: User Table After Verification
section "User Table After Verification"
psql "$DB_URL" -c 'SELECT id, email, is_email_verified FROM "user";'

# SECTION 8: OnBoarding Table After Verification
section "OnBoarding Table After Verification"
psql "$DB_URL" -c 'SELECT user_id, full_name, completed FROM "on_boarding" ORDER BY created_at DESC LIMIT 1;'

# SECTION 9: OTP Table After Verification
section "OTP Table After Verification"
OTP_LEFT=$(psql "$DB_URL" -t -A -c 'SELECT count(*) FROM "otp";')
if [[ "$OTP_LEFT" == "0" ]]; then
  success "OTP table is empty after verification"
else
  fail "OTP table is not empty after verification"
fi

echo -e "${GREEN}\n🎉 End-to-end test completed successfully!${NC}"