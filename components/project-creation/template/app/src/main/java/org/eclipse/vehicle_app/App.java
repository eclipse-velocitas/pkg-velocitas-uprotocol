package org.eclipse.vehicle_app;

import java.util.concurrent.CompletionStage;
import java.util.concurrent.Executor;

import org.covesa.uservice.vehicle.body.horn.v1.ActivateHornRequest;
import org.covesa.uservice.vehicle.body.horn.v1.HornMode;
import org.eclipse.uprotocol.rpc.RpcMapper;
import org.eclipse.uprotocol.rpc.RpcResult;
import org.eclipse.uprotocol.transport.UListener;
import org.eclipse.uprotocol.transport.builder.UAttributesBuilder;
import org.eclipse.uprotocol.ulink.echo.ULink;
import org.eclipse.uprotocol.uri.builder.UResourceBuilder;
import org.eclipse.uprotocol.v1.UAttributes;
import org.eclipse.uprotocol.v1.UCode;
import org.eclipse.uprotocol.v1.UEntity;
import org.eclipse.uprotocol.v1.UPayload;
import org.eclipse.uprotocol.v1.UPayloadFormat;
import org.eclipse.uprotocol.v1.UPriority;
import org.eclipse.uprotocol.v1.UResource;
import org.eclipse.uprotocol.v1.UStatus;
import org.eclipse.uprotocol.v1.UUri;

public class App {

    public App() {
    }

    public void run() {
        // request to be send
        ActivateHornRequest request = ActivateHornRequest.newBuilder().setMode(HornMode.HM_CONTINUOUS).build();

        final UUri mTopic = UUri.newBuilder()
                .setEntity(UEntity.newBuilder().setName("body.horn").setVersionMajor(1))
                .setResource(UResource.newBuilder().setName("hornstatus").setInstance("is_active").setMessage("true"))
                .build();

        final UPayload mPayload = UPayload.newBuilder()
                .setValue(request.toByteString())
                .setFormat(UPayloadFormat.UPAYLOAD_FORMAT_PROTOBUF)
                .build();

        final class MyListener implements UListener {
            @Override
            public UStatus onReceive(UUri uri, UPayload payload, UAttributes attributes) {
                System.out.println("uri: " + uri);
                System.out.println("payload: " + payload);
                return UStatus.newBuilder().setCode(UCode.OK).build();
            }
        }

        ULink ulink = new ULink(new Executor() {
            @Override
            public void execute(Runnable command) {
                command.run();
            }
        });

        ulink.registerListener(mTopic, new MyListener());

        UAttributes attributes = UAttributesBuilder.publish(UPriority.UPRIORITY_CS4).build();

        UStatus status = ulink.send(mTopic, mPayload, attributes);
        System.out.println("Status: " + status.getCode());

        // inovke rpc method

        final UUri uri = UUri.newBuilder()
                .setEntity(UEntity.newBuilder().setName("body.horn").setVersionMajor(1))
                .setResource(UResourceBuilder.forRpcRequest("ActivateHorn")).build();

        final UUri sink = UUri.newBuilder()
                .setEntity(UEntity.newBuilder().setName("vehicle_app").setVersionMajor(1))
                .setResource(UResourceBuilder.forRpcResponse()).build();

        attributes = UAttributesBuilder.request(UPriority.UPRIORITY_CS1, sink, 1000).build();

        // this is just with the test ULink which directly sends back the payload,
        // normally one should expect the response accordingly
        final CompletionStage<RpcResult<ActivateHornRequest>> rpcResponse = RpcMapper.mapResponseToResult(
                ulink.invokeMethod(uri, mPayload, attributes), ActivateHornRequest.class);

        final CompletionStage<Void> test = rpcResponse.thenAccept(RpcResult -> {
            System.out.println("RPC Result: " + RpcResult.isSuccess());
        });
        test.toCompletableFuture().join();
    }
}
