<?php
/**
 * Plugin Name: XMR Payment Gateway
 * Description: Accetta pagamenti in Monero (XMR) senza KYC.
 * Version: 1.0
 * Author: MyZubster
 */

add_action('plugins_loaded', 'init_xmr_gateway');
function init_xmr_gateway() {
    add_filter('woocommerce_payment_gateways', 'add_xmr_gateway');
}

function add_xmr_gateway($gateways) {
    $gateways[] = 'WC_Gateway_XMR';
    return $gateways;
}

class WC_Gateway_XMR extends WC_Payment_Gateway {
    public function __construct() {
        $this->id = 'xmr';
        $this->icon = 'https://getmonero.org/press-kit/symbols/monero-symbol-480.png';
        $this->method_title = 'Monero (XMR)';
        $this->title = 'Monero (XMR)';
        $this->has_fields = false;
        $this->init_form_fields();
        $this->init_settings();
        add_action('woocommerce_update_options_payment_gateways_' . $this->id, array($this, 'process_admin_options'));
    }

    public function process_payment($order_id) {
        $order = wc_get_order($order_id);
        $xmr_address = '4...'; // Inserisci qui il tuo indirizzo XMR
        $amount_xmr = round($order->get_total() / 150, 6); // Tasso di cambio fittizio

        $order->update_status('on-hold', 'In attesa di pagamento XMR');
        wc_reduce_stock_levels($order_id);

        return array(
            'result' => 'success',
            'redirect' => "monero:$xmr_address?amount=$amount_xmr"
        );
    }
}
