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
        System.out.println("Skeleton for uApplication");
    }
}
