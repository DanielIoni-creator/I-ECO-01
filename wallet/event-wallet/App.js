import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  Alert,
  ActivityIndicator,
  Clipboard,
  Share
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

const WalletApp = () => {
  const [wallet, setWallet] = useState(null);
  const [address, setAddress] = useState('');
  const [balance, setBalance] = useState('0');
  const [seed, setSeed] = useState('');
  const [amount, setAmount] = useState('');
  const [recipient, setRecipient] = useState('');
  const [loading, setLoading] = useState(false);
  const [transactions, setTransactions] = useState([]);

  // Carica wallet salvato all'avvio
  useEffect(() => {
    loadWallet();
  }, []);

  const generateSeed = () => {
    const words = [
      'acid', 'alien', 'alpha', 'angel', 'audio', 'basic', 'blade', 'chain',
      'cyber', 'dark', 'dawn', 'echo', 'edge', 'fire', 'flame', 'focus',
      'ghost', 'glass', 'grid', 'hack', 'icon', 'ionic', 'laser', 'matrix',
      'neon', 'nova', 'optic', 'pulse', 'quantum', 'radio', 'shadow', 'signal',
      'stealth', 'storm', 'synth', 'trace', 'ultra', 'vault', 'vector', 'viral',
      'voltage', 'wave', 'wire', 'xeno', 'zero', 'zone'
    ];
    let seed = '';
    for (let i = 0; i < 12; i++) {
      seed += words[Math.floor(Math.random() * words.length)] + ' ';
    }
    return seed.trim();
  };

  const createWallet = async () => {
    setLoading(true);
    try {
      // Simula creazione wallet (in produzione usare monero-javascript)
      const newSeed = generateSeed();
      const newAddress = '4' + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
      
      setSeed(newSeed);
      setAddress(newAddress);
      setWallet({ address: newAddress, seed: newSeed });
      
      await AsyncStorage.setItem('wallet', JSON.stringify({ 
        address: newAddress, 
        seed: newSeed 
      }));
      
      Alert.alert('✅ Wallet creato!', `Indirizzo: ${newAddress}`);
    } catch (error) {
      Alert.alert('❌ Errore', error.message);
    } finally {
      setLoading(false);
    }
  };

  const loadWallet = async () => {
    try {
      const saved = await AsyncStorage.getItem('wallet');
      if (saved) {
        const data = JSON.parse(saved);
        setWallet(data);
        setAddress(data.address);
        setSeed(data.seed);
      }
    } catch (error) {
      console.error('Errore caricamento wallet:', error);
    }
  };

  const getBalance = async () => {
    if (!wallet) {
      Alert.alert('⚠️ Crea prima un wallet');
      return;
    }
    setLoading(true);
    try {
      // Simula recupero saldo (in produzione usare RPC)
      const fakeBalance = (Math.random() * 10).toFixed(6);
      setBalance(fakeBalance);
      
      // Aggiungi transazione fittizia
      const newTx = {
        id: Date.now(),
        type: 'received',
        amount: fakeBalance,
        timestamp: new Date().toISOString(),
        address: address
      };
      setTransactions([newTx, ...transactions]);
    } catch (error) {
      Alert.alert('❌ Errore', error.message);
    } finally {
      setLoading(false);
    }
  };

  const sendPayment = async () => {
    if (!wallet) {
      Alert.alert('⚠️ Crea prima un wallet');
      return;
    }
    if (!recipient || !amount || parseFloat(amount) <= 0) {
      Alert.alert('⚠️ Inserisci destinatario e importo');
      return;
    }
    
    setLoading(true);
    try {
      // Simula invio pagamento
      const txId = 'tx_' + Math.random().toString(36).substring(2, 15);
      
      const newTx = {
        id: txId,
        type: 'sent',
        amount: amount,
        recipient: recipient,
        timestamp: new Date().toISOString(),
        status: 'confirmed'
      };
      setTransactions([newTx, ...transactions]);
      
      Alert.alert('✅ Pagamento inviato!', `ID: ${txId}`);
      setAmount('');
      setRecipient('');
    } catch (error) {
      Alert.alert('❌ Errore', error.message);
    } finally {
      setLoading(false);
    }
  };

  const copyAddress = () => {
    Clipboard.setString(address);
    Alert.alert('✅ Copiato!', 'Indirizzo copiato negli appunti');
  };

  const shareAddress = () => {
    Share.share({
      message: `💰 MyZubster Wallet\nIndirizzo: ${address}\n\nInvia XMR a questo indirizzo per partecipare all'evento!`
    });
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>💰 Event Wallet</Text>
        <Text style={styles.subtitle}>XMR 1-Click per Eventi</Text>
      </View>

      {!wallet ? (
        <View style={styles.card}>
          <Text style={styles.cardTitle}>Nessun wallet</Text>
          <Text style={styles.cardText}>Crea un nuovo wallet per iniziare</Text>
          <TouchableOpacity style={styles.button} onPress={createWallet} disabled={loading}>
            {loading ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <Text style={styles.buttonText}>🔄 Crea Wallet</Text>
            )}
          </TouchableOpacity>
        </View>
      ) : (
        <>
          <View style={styles.card}>
            <Text style={styles.cardTitle}>📤 Indirizzo</Text>
            <Text style={styles.address}>{address}</Text>
            <View style={styles.rowButtons}>
              <TouchableOpacity style={styles.smallButton} onPress={copyAddress}>
                <Text style={styles.smallButtonText}>📋 Copia</Text>
              </TouchableOpacity>
              <TouchableOpacity style={styles.smallButton} onPress={shareAddress}>
                <Text style={styles.smallButtonText}>📤 Condividi</Text>
              </TouchableOpacity>
            </View>
          </View>

          <View style={styles.card}>
            <Text style={styles.cardTitle}>💰 Saldo</Text>
            <Text style={styles.balance}>{balance} XMR</Text>
            <TouchableOpacity style={styles.button} onPress={getBalance} disabled={loading}>
              {loading ? (
                <ActivityIndicator color="#fff" />
              ) : (
                <Text style={styles.buttonText}>🔄 Aggiorna Saldo</Text>
              )}
            </TouchableOpacity>
          </View>

          <View style={styles.card}>
            <Text style={styles.cardTitle}>💸 Invia Pagamento</Text>
            <TextInput
              style={styles.input}
              placeholder="Indirizzo destinatario"
              value={recipient}
              onChangeText={setRecipient}
              autoCapitalize="none"
            />
            <TextInput
              style={styles.input}
              placeholder="Importo (XMR)"
              value={amount}
              onChangeText={setAmount}
              keyboardType="decimal-pad"
            />
            <TouchableOpacity style={[styles.button, styles.sendButton]} onPress={sendPayment} disabled={loading}>
              {loading ? (
                <ActivityIndicator color="#fff" />
              ) : (
                <Text style={styles.buttonText}>💸 Invia Pagamento</Text>
              )}
            </TouchableOpacity>
          </View>

          <View style={styles.card}>
            <Text style={styles.cardTitle}>📋 Seed (salva in un luogo sicuro!)</Text>
            <Text style={styles.seed}>{seed}</Text>
          </View>
        </>
      )}

      {transactions.length > 0 && (
        <View style={styles.card}>
          <Text style={styles.cardTitle}>📜 Transazioni Recenti</Text>
          {transactions.slice(0, 5).map((tx) => (
            <View key={tx.id} style={styles.txItem}>
              <Text style={tx.type === 'received' ? styles.txReceived : styles.txSent}>
                {tx.type === 'received' ? '📥 Ricevuto' : '📤 Inviato'}
              </Text>
              <Text style={styles.txAmount}>{tx.amount} XMR</Text>
              <Text style={styles.txDate}>{new Date(tx.timestamp).toLocaleDateString()}</Text>
            </View>
          ))}
        </View>
      )}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0A0A0A',
    padding: 20,
  },
  header: {
    marginVertical: 20,
    alignItems: 'center',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#8B00FF',
  },
  subtitle: {
    fontSize: 16,
    color: '#C0C0C0',
  },
  card: {
    backgroundColor: '#1A1A1A',
    borderRadius: 15,
    padding: 20,
    marginVertical: 10,
    borderWidth: 1,
    borderColor: '#333',
  },
  cardTitle: {
    color: '#8B00FF',
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  cardText: {
    color: '#C0C0C0',
    fontSize: 14,
    marginBottom: 10,
  },
  address: {
    color: '#FFFFFF',
    fontSize: 14,
    fontFamily: 'monospace',
    backgroundColor: '#0A0A0A',
    padding: 10,
    borderRadius: 8,
    marginBottom: 10,
  },
  balance: {
    color: '#8B00FF',
    fontSize: 32,
    fontWeight: 'bold',
    textAlign: 'center',
    padding: 10,
  },
  seed: {
    color: '#FF6600',
    fontSize: 14,
    fontFamily: 'monospace',
    backgroundColor: '#0A0A0A',
    padding: 10,
    borderRadius: 8,
  },
  input: {
    backgroundColor: '#0A0A0A',
    color: '#FFFFFF',
    padding: 12,
    borderRadius: 8,
    marginBottom: 10,
    borderWidth: 1,
    borderColor: '#333',
  },
  button: {
    backgroundColor: '#8B00FF',
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
  },
  sendButton: {
    backgroundColor: '#FF6600',
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
  },
  smallButton: {
    backgroundColor: '#333',
    padding: 10,
    borderRadius: 8,
    flex: 1,
    marginHorizontal: 5,
    alignItems: 'center',
  },
  smallButtonText: {
    color: '#FFFFFF',
    fontSize: 14,
  },
  rowButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  txItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    padding: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#333',
  },
  txReceived: {
    color: '#00FF88',
  },
  txSent: {
    color: '#FF6600',
  },
  txAmount: {
    color: '#FFFFFF',
  },
  txDate: {
    color: '#666',
    fontSize: 12,
  },
});

export default WalletApp;
