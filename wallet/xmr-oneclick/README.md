# XMR Wallet 1-Click

## Descrizione
App per creare wallet Monero e pagare la crew. No KYC.

## Tecnologie
- React Native / Expo
- monero-javascript
- AsyncStorage

## Installazione
```bash
npm install
npx expo start

### **2️⃣ Aggiungi il codice principale**

```bash
cat > wallet/xmr-oneclick/App.js << 'EOF'
import React, { useState } from 'react';
import { View, Text, Button, StyleSheet, Alert, ScrollView } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function App() {
  const [wallet, setWallet] = useState(null);
  const [address, setAddress] = useState('');
  const [balance, setBalance] = useState('0');
  const [seed, setSeed] = useState('');

  const createWallet = async () => {
    try {
      // Simula creazione wallet (in produzione usare monero-javascript)
      const newAddress = '4' + Math.random().toString(36).substring(2, 15);
      const newSeed = 'acid ' + Math.random().toString(36).substring(2, 8) + ' ' + Math.random().toString(36).substring(2, 8);
      
      setAddress(newAddress);
      setSeed(newSeed);
      setWallet({ address: newAddress, seed: newSeed });
      
      await AsyncStorage.setItem('wallet', JSON.stringify({ address: newAddress, seed: newSeed }));
      Alert.alert('✅ Wallet creato!', `Indirizzo: ${newAddress}`);
    } catch (error) {
      Alert.alert('❌ Errore', error.message);
    }
  };

  const getBalance = async () => {
    if (!wallet) {
      Alert.alert('⚠️ Crea prima un wallet');
      return;
    }
    try {
      // Simula recupero saldo
      const fakeBalance = (Math.random() * 10).toFixed(6);
      setBalance(fakeBalance);
    } catch (error) {
      Alert.alert('❌ Errore', error.message);
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
        Alert.alert('✅ Wallet caricato!');
      }
    } catch (error) {
      Alert.alert('❌ Errore', error.message);
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>💰 XMR Wallet 1-Click</Text>
      
      <View style={styles.card}>
        <Button title="Crea Nuovo Wallet" onPress={createWallet} color="#8B00FF" />
        <View style={styles.spacer} />
        <Button title="Carica Wallet Salvato" onPress={loadWallet} color="#6200EE" />
        <View style={styles.spacer} />
        <Button title="Aggiorna Saldo" onPress={getBalance} color="#3700B3" />
      </View>

      {address ? (
        <View style={styles.card}>
          <Text style={styles.label}>📤 Indirizzo:</Text>
          <Text style={styles.value}>{address}</Text>
          <Text style={styles.label}>🔑 Seed:</Text>
          <Text style={styles.value}>{seed}</Text>
          <Text style={styles.label}>💰 Saldo:</Text>
          <Text style={styles.balance}>{balance} XMR</Text>
        </View>
      ) : (
        <Text style={styles.hint}>Crea o carica un wallet per iniziare</Text>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    padding: 20,
    backgroundColor: '#0A0A0A',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    textAlign: 'center',
    marginVertical: 20,
    color: '#8B00FF',
  },
  card: {
    backgroundColor: '#1A1A1A',
    borderRadius: 15,
    padding: 20,
    marginVertical: 10,
    borderWidth: 1,
    borderColor: '#333',
  },
  label: {
    color: '#C0C0C0',
    fontSize: 14,
    marginTop: 10,
  },
  value: {
    color: '#FFFFFF',
    fontSize: 16,
    fontFamily: 'monospace',
    backgroundColor: '#0A0A0A',
    padding: 10,
    borderRadius: 8,
    marginTop: 5,
  },
  balance: {
    color: '#8B00FF',
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    padding: 10,
  },
  hint: {
    color: '#666',
    textAlign: 'center',
    marginTop: 30,
    fontSize: 16,
  },
  spacer: {
    height: 10,
  },
});
