/**
 * AirAsia Search URL Builder
 * Constructs direct URLs to AirAsia search results pages
 * Bypasses form automation entirely
 */

/**
 * Build AirAsia search URL from flight parameters
 * @param {string} origin - Origin airport code (e.g., 'BKK', 'Bangkok')
 * @param {string} destination - Destination airport code (e.g., 'CNX', 'Chiang Mai')
 * @param {string} departDate - Departure date in DD/MM/YYYY or YYYY-MM-DD format
 * @param {Object} options - Optional parameters
 * @param {string} options.tripType - 'O' for one-way, 'R' for round-trip (default: 'O')
 * @param {string} options.returnDate - Return date (required if tripType is 'R')
 * @param {number} options.adult - Number of adults (default: 1)
 * @param {number} options.child - Number of children (default: 0)
 * @param {number} options.infant - Number of infants (default: 0)
 * @param {string} options.currency - Currency code (default: 'THB')
 * @returns {string} Complete AirAsia search URL
 */
function buildAirAsiaSearchUrl(origin, destination, departDate, options = {}) {
    // Default options
    const {
        tripType = 'O',
        returnDate = null,
        adult = 1,
        child = 0,
        infant = 0,
        currency = 'THB'
    } = options;

    // Normalize airport codes (extract 3-letter code if full name provided)
    const normalizeAirportCode = (input) => {
        // If it's already a 3-letter code, return as-is
        if (/^[A-Z]{3}$/i.test(input.trim())) {
            return input.trim().toUpperCase();
        }

        // Common airport mappings
        const airportMap = {
            'bangkok': 'BKK',
            'chiang mai': 'CNX',
            'phuket': 'HKT',
            'krabi': 'KBV',
            'koh samui': 'USM',
            'hat yai': 'HDY',
            'singapore': 'SIN',
            'kuala lumpur': 'KUL',
            'penang': 'PEN',
            'langkawi': 'LGK',
            'jakarta': 'CGK',
            'bali': 'DPS',
            'manila': 'MNL',
            'cebu': 'CEB',
            'hong kong': 'HKG',
            'taipei': 'TPE',
            'seoul': 'ICN',
            'tokyo': 'NRT',
            'osaka': 'KIX'
        };

        const normalized = input.toLowerCase().trim();
        return airportMap[normalized] || input.trim().toUpperCase();
    };

    // Normalize date format to DD/MM/YYYY
    const normalizeDate = (dateStr) => {
        if (!dateStr) return null;

        let day, month, year;

        if (dateStr.includes('-')) {
            // YYYY-MM-DD format
            [year, month, day] = dateStr.split('-');
        } else if (dateStr.includes('/')) {
            // DD/MM/YYYY format
            [day, month, year] = dateStr.split('/');
        } else {
            throw new Error(`Invalid date format: ${dateStr}. Use DD/MM/YYYY or YYYY-MM-DD`);
        }

        // Ensure proper padding
        day = day.padStart(2, '0');
        month = month.padStart(2, '0');

        return `${day}/${month}/${year}`;
    };

    // Process inputs
    const originCode = normalizeAirportCode(origin);
    const destCode = normalizeAirportCode(destination);
    const formattedDepartDate = normalizeDate(departDate);
    const formattedReturnDate = returnDate ? normalizeDate(returnDate) : null;

    // Validate required parameters
    if (!originCode || originCode.length !== 3) {
        throw new Error(`Invalid origin airport code: ${origin}`);
    }
    if (!destCode || destCode.length !== 3) {
        throw new Error(`Invalid destination airport code: ${destination}`);
    }
    if (!formattedDepartDate) {
        throw new Error('Departure date is required');
    }
    if (tripType === 'R' && !formattedReturnDate) {
        throw new Error('Return date is required for round-trip flights');
    }

    // Build URL parameters
    const params = new URLSearchParams({
        origin: originCode,
        destination: destCode,
        departDate: formattedDepartDate,
        tripType: tripType,
        adult: adult.toString(),
        locale: 'en-gb',
        currency: currency
    });

    // Add optional parameters
    if (child > 0) params.set('child', child.toString());
    if (infant > 0) params.set('infant', infant.toString());
    if (formattedReturnDate) params.set('returnDate', formattedReturnDate);

    // Construct full URL
    const baseUrl = 'https://www.airasia.com/flights/search/';
    const fullUrl = `${baseUrl}?${params.toString()}`;

    console.log('[URL Builder] Generated URL:', fullUrl);
    console.log('[URL Builder] Parameters:', {
        origin: originCode,
        destination: destCode,
        departDate: formattedDepartDate,
        returnDate: formattedReturnDate,
        tripType,
        passengers: { adult, child, infant },
        currency
    });

    return fullUrl;
}

// Export for use
window.buildAirAsiaSearchUrl = buildAirAsiaSearchUrl;

// Example usage:
// buildAirAsiaSearchUrl('Bangkok', 'Chiang Mai', '20/02/2026')
// buildAirAsiaSearchUrl('BKK', 'CNX', '2026-02-20', { tripType: 'R', returnDate: '2026-02-25' })
